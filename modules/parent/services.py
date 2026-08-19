from common.schemas import GenericResponse
from modules.parent.models import Parent
from modules.parent.schemas import ParentCreate, ParentResponse
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
import csv
import io
from fastapi import UploadFile
router = APIRouter()

async def parent_create(parent: ParentCreate, db: AsyncSession):
    new_user = User(
        first_name=parent.first_name,
        last_name=parent.last_name,
        email=parent.email,
        phone_number=parent.phone_number,
        is_staff=False,
        is_active=True
    )

    db.add(new_user)
    await db.flush()

    new_parent = Parent(
        user_id=new_user.id,
        occupation=parent.occupation,
        address=parent.address
    )

    db.add(new_parent)
    await db.flush()
    parent_id = new_parent.id

    await db.commit()

    result = await db.execute(
        select(Parent)
        .options(selectinload(Parent.user))
        .where(Parent.id == parent_id)
    )

    parent_data = result.scalar_one()

    return GenericResponse(
        success=True,
        message="Parent created successfully",
        data = ParentResponse(
            id=parent_data.id,
            first_name=parent_data.user.first_name,
            last_name=parent_data.user.last_name,
            email=parent_data.user.email,
            phone_number=parent_data.user.phone_number,
            occupation=parent_data.occupation,
            address=parent_data.address,
        )
    )

async def get_parent(parent_id: int, db: AsyncSession):

    result = await db.execute(
        select(Parent)
        .options(selectinload(Parent.user))
        .where(Parent.id == parent_id)
    )

    parent = result.scalar_one_or_none()

    if parent is None:
        raise HTTPException(
            status_code=404,
            detail="Parent not found"
        )

    parent_response = ParentResponse(
        id=parent.id,
        first_name=parent.user.first_name,
        last_name=parent.user.last_name,
        email=parent.user.email,
        phone_number=parent.user.phone_number,
        occupation=parent.occupation,
        address=parent.address,
    )

    return GenericResponse(
        success=True,
        message="Parent fetched successfully",
        data=parent_response
    )

async def parents_list(parent_id: int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Parent).options(selectinload(Parent.user)))
    parents = result.scalars().all()
    parent_responses = []

    for parent in parents:
        parent_response = ParentResponse(
            id=parent.id,
            first_name=parent.user.first_name,
            last_name=parent.user.last_name,
            email=parent.user.email,
            phone_number=parent.user.phone_number,
            occupation=parent.occupation,
            address=parent.address,
        )

        parent_responses.append(parent_response)

    return GenericResponse(
        success=True,
        message="Parent records retrieved successfully",
        data=parent_responses
    )

async def parent_bulk_upload(file: UploadFile,db: AsyncSession):
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

        new_parent = Parent(
            user_id=new_user.id,
            occupation=row["occupation"],
            address=row["address"]
        )

        db.add(new_parent)

    await db.commit()
    return GenericResponse(
            success=True,
            message="Parents uploaded successfully",
            data=None
    )