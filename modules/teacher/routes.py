from common.schemas import GenericResponse
from modules.parent.schemas import ParentResponse, ParentCreate
from modules.parent.services import parent_create, get_parent
from modules.teacher.schemas import TeacherResponse,TeacherCreate
from modules.student.models import Student,StudentTeacher,StudentParent
from sqlalchemy import select
from modules.student import services
from fastapi import Depends,APIRouter,HTTPException
from common.database import engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import selectinload
from common.pagination import PaginationParams
from modules.teacher.services import update_student, teacher_create, teacher_get
from fastapi import UploadFile, File,Depends
from modules.teacher.services import teacher_bulk_upload
from common.security import get_current_user, require_role
from modules.user.models import User

AsyncSessionLocal = async_sessionmaker(bind=engine)
# db = AsyncSessionLocal()

router = APIRouter()

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

@router.post("/teachers",response_model=GenericResponse[TeacherResponse])
async def create_teacher(teacher: TeacherCreate,db: AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin"))):
    return await teacher_create(teacher, db)

@router.get("/teachers/{teacher_id}",response_model=GenericResponse[TeacherResponse])
async def get_teacher(teacher_id: int,db: AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin","teacher","parent"))):
    return await teacher_get(teacher_id, db)

@router.post("/teachers/upload")
async def upload_teachers(file: UploadFile = File(...),db:AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin"))):
    return await teacher_bulk_upload(file, db)
