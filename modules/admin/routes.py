from common.schemas import GenericResponse
from modules.admin.schemas import AdminResponse, AdminCreate
from modules.admin.services import admin_create, admin_get
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

AsyncSessionLocal = async_sessionmaker(bind=engine)
# db = AsyncSessionLocal()

router = APIRouter()

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

@router.post("/admin",response_model=GenericResponse[AdminResponse])
async def create_admin(admin: AdminCreate,db: AsyncSession = Depends(get_db)):
    return await admin_create(admin, db)

@router.get("/admin",response_model=GenericResponse[AdminResponse])
async def get_admin(db: AsyncSession = Depends(get_db)):
    return await admin_get(db)
