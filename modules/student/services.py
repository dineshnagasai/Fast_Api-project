from common.schemas import GenericResponse
from modules.parent.models import Parent
from modules.student.schemas import StudentResponse,StudentCreate
from modules.student.models import Student,StudentTeacher,StudentParent
from sqlalchemy import select
from fastapi import Depends,APIRouter,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import selectinload
from common.database import get_db
from common.pagination import PaginationParams
from modules.student.validation import validate_student_exists
from modules.teacher.models import Teacher
from modules.user.models import User
from fastapi import UploadFile
import csv
import io

router = APIRouter()

async def get_student(student_id: int,db: AsyncSession,current_user:User):
    # raise Exception("Testing global exception handler")
    result = await db.execute(select(Student).options(selectinload(Student.user),
            selectinload(Student.parent_link).selectinload(StudentParent.linked_parent).selectinload(Parent.user),
            selectinload(Student.teacher_link).selectinload(StudentTeacher.linked_teacher).selectinload(Teacher.user)).
                              where(Student.id == student_id))
    student = result.scalars().one_or_none()
    if student is None:
        raise HTTPException(status_code=404,detail="Student not found")

    if current_user.role in ("admin", "teacher"):
        return student

    if current_user.role == "student":
        if student.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only access your own student record"
            )
    elif current_user.role in ("admin", "teacher"):
        pass

    elif current_user.role == "parent":
        pass

    parent_names = [link.linked_parent.user.first_name for link in student.parent_link]
    teacher_ids  = [link.linked_teacher.id for link in student.teacher_link]

    student_response = StudentResponse(
        id=student.id,
        first_name=student.user.first_name,
        last_name=student.user.last_name,
        department=student.department,
        email=student.user.email,
        phone_number=student.user.phone_number,
        age = student.age,
        parents=parent_names,
        teacher_ids=teacher_ids
    )
    return GenericResponse(
        success=True,
        message="Student record retrieved successfully",
        data=student_response
    )

async def students_list( pagination: PaginationParams = Depends(),db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).options(
         selectinload(Student.user),
                    selectinload(Student.parent_link).selectinload(StudentParent.linked_parent).selectinload(Parent.user),
                    selectinload(Student.teacher_link).selectinload(StudentTeacher.linked_teacher)).offset(pagination.offset).limit(pagination.size))

    student_list = result.scalars().all()
    student_responses= []
    for student in student_list:
        parent_names = [link.linked_parent.name for link in student.parent_link]
        teacher_ids = [link.linked_teacher.id for link in student.teacher_link]
        student_response = StudentResponse(
            id=student.id,
            first_name=student.user.first_name,
            last_name=student.user.last_name,
            age=student.age,
            department=student.department,
            email=student.user.email,
            phone_number=student.user.phone_number,
            parents=parent_names,
            teacher_ids=teacher_ids
        )
        student_responses.append(student_response)

    return GenericResponse(
        success=True,
        message="Student records retrieved successfully",
        data=student_responses
    )

#put validations in validation.py
async def student_create(student:StudentCreate,db: AsyncSession = Depends(get_db)):
    new_user = User(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        phone_number=student.phone_number,
        is_staff=False,
        is_active=True
    )
    db.add(new_user)
    await db.flush()

    new_student = Student(
                            user_id = new_user.id,
                            age = student.age,
                            department = student.department)

    db.add(new_student)
    await db.commit()

    # Fetch student with user relationship
    result = await db.execute(
        select(Student)
        .options(selectinload(Student.user))
        .where(Student.id == new_student.id)
    )
    student = result.scalars().one_or_none()
    # await db.refresh(new_student)
    return GenericResponse(
                            success=True,
                            message="Student created successfully",
                            data=StudentResponse(
                                id=student.id,
                                first_name=student.user.first_name,
                                last_name=student.user.last_name,
                                email=student.user.email,
                                phone_number=student.user.phone_number,
                                age=student.age,
                                department=student.department,
                            )
                          )
#Put function
async def update_student(student_id: int,student: StudentCreate,db:AsyncSession):

    existing_student = await validate_student_exists(student_id,db)
    existing_student.name = student.name
    existing_student.age = student.age
    existing_student.department = student.department
    existing_student.email = student.email
    existing_student.is_active = student.is_active

    await db.commit()
    await db.refresh(existing_student)
    return GenericResponse(
        success =  True,
        message =  "Student record updated successfully",
        data    =  existing_student
    )

async def student_bulk_upload(file: UploadFile,db: AsyncSession):
    contents = await file.read()
    csv_file = io.StringIO(contents.decode("utf-8"))
    reader = csv.DictReader(csv_file)
    for row in reader:
        new_user = User(
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row["email"],
            phone_number=row["phone_number"],
            is_staff=False,
            is_active=True
        )

        db.add(new_user)
        await db.flush()

        new_student = Student(
            user_id=new_user.id,
            age=int(row["age"]),
            department=row["department"]
        )

        db.add(new_student)
    await db.commit()
    return GenericResponse(
        success=True,
        message="Students uploaded successfully",
        data=None
    )