from common.schemas import GenericResponse
from modules.attendance.schemas import TeacherAttendanceResponse, TeacherAttendanceCreate, StudentAttendanceResponse, \
    StudentAttendanceCreate
from modules.attendance.services import teacher_attendance_create, student_attendance_create
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

@router.post("/teacher-attendance",response_model=GenericResponse[TeacherAttendanceResponse])
async def create_teacher_attendance(attendance: TeacherAttendanceCreate,db: AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin"))):
    return await teacher_attendance_create(attendance, db)

@router.post("/student-attendance",response_model=GenericResponse[StudentAttendanceResponse])
async def create_student_attendance(attendance: StudentAttendanceCreate,db: AsyncSession = Depends(get_db),current_user: User = Depends(require_role("admin"))):
    return await student_attendance_create(attendance, db)