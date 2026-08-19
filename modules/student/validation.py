from modules.student.schemas import StudentResponse,StudentCreate
from modules.student.models import Student,StudentTeacher,StudentParent
from sqlalchemy import select
from fastapi import Depends,APIRouter,HTTPException
from common.database import engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

AsyncSessionLocal = async_sessionmaker(bind=engine)

router = APIRouter()

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

async def validate_student_exists(student_id: int,db: AsyncSession):
    result = await db.execute(select(Student).where(Student.id == student_id))

    existing_student = result.scalar_one_or_none()

    if existing_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return existing_student