from common.schemas import GenericResponse
from modules.parent.schemas import ParentResponse, ParentCreate
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
from fastapi import UploadFile, File
from modules.student.services import student_bulk_upload
from common.security import get_current_user, require_admin,require_role
from modules.user.models import User

AsyncSessionLocal = async_sessionmaker(bind=engine)

router = APIRouter()

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

@router.get("/students/{student_id}",response_model=GenericResponse[StudentResponse])
async def get_student_record(student_id: int,db: AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin","teacher","parent","student"))):
    return await get_student(student_id,db,current_user)

@router.get("/students",response_model=GenericResponse[list[StudentResponse]])
async def get_students_list( pagination: PaginationParams = Depends(),db: AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin,teacher"))):
    return await students_list(pagination,db)

@router.post("/students",response_model=GenericResponse[StudentResponse])
async def create_student(student:StudentCreate,db: AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin"))):
    return await student_create(student,db)

@router.put("/students/{student_id}", response_model=GenericResponse[StudentResponse])
async def update_student(student_id: int,student: StudentCreate,db: AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin"))):
    return await services.update_student(student_id,student,db)

@router.post("/students/upload")
async def upload_students(file: UploadFile = File(...),db: AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin"))):
    return await student_bulk_upload(file, db)