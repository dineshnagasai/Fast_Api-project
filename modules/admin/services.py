from common.schemas import GenericResponse
from modules.admin.models import Admin
from modules.admin.schemas import AdminResponse,AdminCreate
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

async def admin_create(admin: AdminCreate, db: AsyncSession):

    new_user = User(
        first_name=admin.first_name,
        last_name=admin.last_name,
        email=admin.email,
        phone_number=admin.phone_number,
        is_staff=True,
        is_active=True
    )

    db.add(new_user)
    await db.flush()

    new_admin = Admin(
        user_id=new_user.id,
        designation=admin.designation
    )

    db.add(new_admin)
    await db.flush()

    admin_id = new_admin.id
    await db.commit()

    result = await db.execute(
        select(Admin)
        .options(selectinload(Admin.user))
        .where(Admin.id == admin_id)
    )

    admin_data = result.scalar_one()

    return GenericResponse(
        success=True,
        message="Admin created successfully",
        data=AdminResponse(
            id=admin_data.id,
            first_name=admin_data.user.first_name,
            last_name=admin_data.user.last_name,
            email=admin_data.user.email,
            phone_number=admin_data.user.phone_number,
            designation=admin_data.designation,
        )
    )

async def admin_get(db: AsyncSession):

    result = await db.execute(
        select(Admin).options(selectinload(Admin.user))
    )

    admin = result.scalar_one_or_none()

    if admin is None:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    return GenericResponse(
        success=True,
        message="Admin retrieved successfully",
        data=AdminResponse(
            id=admin.id,
            first_name=admin.user.first_name,
            last_name=admin.user.last_name,
            email=admin.user.email,
            phone_number=admin.user.phone_number,
            designation=admin.designation,
        )
    )