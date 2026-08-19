from common.schemas import GenericResponse
from modules.parent.schemas import ParentResponse, ParentCreate
from modules.parent.services import parent_create, get_parent, parents_list
from modules.student.schemas import StudentResponse,StudentCreate
from modules.student.models import Student,StudentTeacher,StudentParent
from sqlalchemy import select
from modules.student import services
from fastapi import Depends,APIRouter,HTTPException
from common.database import engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import selectinload
from common.pagination import PaginationParams
from modules.parent.services import parent_create,get_parent,parents_list
from fastapi import UploadFile, File
from modules.parent.services import parent_bulk_upload
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

@router.post("/parents",response_model=GenericResponse[ParentResponse])
async def create_parent(parent:ParentCreate,db: AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin"))):
    return await parent_create(parent,db)

@router.get("/parents/{parent_id}",response_model=GenericResponse[ParentResponse])
async def parent_get(parent_id: int,db: AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin","parent"))):
    return await get_parent(parent_id,db)

@router.get("/parents",response_model=GenericResponse[list[ParentResponse]])
async def get_parents_list( pagination: PaginationParams = Depends(),db: AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin"))):
    return await parents_list(pagination,db)

@router.post("/parents/upload")
async def upload_parents(file: UploadFile = File(...),db:AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin"))):
    return await parent_bulk_upload(file, db)
