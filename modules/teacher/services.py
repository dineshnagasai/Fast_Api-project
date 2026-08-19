from common.schemas import GenericResponse
from modules.teacher.models import Teacher
from modules.teacher.schemas import TeacherResponse, TeacherCreate
from modules.parent.services import parent_create, get_parent
from modules.student.schemas import StudentResponse,StudentCreate
from modules.student.models import Student,StudentTeacher,StudentParent
from sqlalchemy import select
from modules.student import services
from fastapi import Depends,APIRouter,HTTPException
from common.database import engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import selectinload
from common.pagination import PaginationParams
from modules.student.services import update_student, student_create, get_student, students_list
from modules.user.models import User
import csv
import io
from fastapi import UploadFile

async def teacher_create(teacher: TeacherCreate, db: AsyncSession):

    new_user = User(
        first_name=teacher.first_name,
        last_name=teacher.last_name,
        email=teacher.email,
        phone_number=teacher.phone_number,
        is_staff=True,
        is_active=True
    )

    db.add(new_user)
    await db.flush()

    new_teacher = Teacher(
        user_id=new_user.id,
        subject=teacher.subject,
        qualification=teacher.qualification
    )

    db.add(new_teacher)
    await db.flush()

    teacher_id = new_teacher.id

    await db.commit()

    result = await db.execute(
        select(Teacher)
        .options(selectinload(Teacher.user))
        .where(Teacher.id == teacher_id)
    )

    teacher_data = result.scalar_one()

    return GenericResponse(
        success=True,
        message="Teacher created successfully",
        data=TeacherResponse(
            id=teacher_data.id,
            first_name=teacher_data.user.first_name,
            last_name=teacher_data.user.last_name,
            email=teacher_data.user.email,
            phone_number=teacher_data.user.phone_number,
            subject=teacher_data.subject,
            qualification=teacher_data.qualification,
        )
    )

async def teacher_get(teacher_id: int, db: AsyncSession):

    result = await db.execute(
        select(Teacher)
        .options(selectinload(Teacher.user))
        .where(Teacher.id == teacher_id)
    )

    teacher = result.scalar_one_or_none()

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    teacher_response = TeacherResponse(
        id=teacher.id,
        first_name=teacher.user.first_name,
        last_name=teacher.user.last_name,
        email=teacher.user.email,
        phone_number=teacher.user.phone_number,
        subject=teacher.subject,
        qualification=teacher.qualification,
    )

    return GenericResponse(
        success=True,
        message="Teacher fetched successfully",
        data=teacher_response
    )

async def teacher_bulk_upload(file: UploadFile,db: AsyncSession):
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

        new_parent = Teacher(
            user_id=new_user.id,
            subject=row["subject"],
            qualification=row["qualification"]
        )

        db.add(new_parent)

    await db.commit()
    return GenericResponse(
            success=True,
            message="Parents uploaded successfully",
            data=None
    )