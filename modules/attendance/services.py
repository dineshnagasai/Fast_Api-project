from common.schemas import GenericResponse
from modules.parent.models import Parent
from modules.attendance.schemas import TeacherAttendanceCreate,TeacherAttendanceResponse,StudentAttendanceCreate,StudentAttendanceResponse
from modules.attendance.models import TeacherAttendance,StudentAttendance
from sqlalchemy import select
from fastapi import Depends,APIRouter,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import selectinload
from common.database import get_db
from common.pagination import PaginationParams
from modules.student.models import Student
from modules.student.validation import validate_student_exists
from modules.teacher.models import Teacher
from modules.user.models import User

async def teacher_attendance_create(attendance: TeacherAttendanceCreate,db: AsyncSession):
    # Verify teacher exists
    result = await db.execute(select(Teacher).where(Teacher.id == attendance.teacher_id))

    teacher = result.scalar_one_or_none()

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    # Create attendance
    new_attendance = TeacherAttendance(
        date=attendance.date,
        status=attendance.status,
        check_in=attendance.check_in,
        check_out=attendance.check_out,
        remarks=attendance.remarks,
        teacher_id=attendance.teacher_id
    )

    db.add(new_attendance)
    await db.flush()

    attendance_id = new_attendance.id

    await db.commit()

    result = await db.execute(
        select(TeacherAttendance)
        .where(TeacherAttendance.id == attendance_id)
    )

    attendance_data = result.scalar_one()

    return GenericResponse(
        success=True,
        message="Teacher attendance marked successfully",
        data=TeacherAttendanceResponse(
            id=attendance_data.id,
            date=attendance_data.date,
            status=attendance_data.status,
            check_in=attendance_data.check_in,
            check_out=attendance_data.check_out,
            remarks=attendance_data.remarks,
            teacher_id=attendance_data.teacher_id,
        )
    )

async def student_attendance_create(attendance: StudentAttendanceCreate,db: AsyncSession):
    # Verify student exists
    result = await db.execute(select(Student).where(Student.id == attendance.student_id))

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Create attendance
    new_attendance = StudentAttendance(
        date=attendance.date,
        status=attendance.status,
        check_in=attendance.check_in,
        check_out=attendance.check_out,
        remarks=attendance.remarks,
        student_id=attendance.student_id
    )

    db.add(new_attendance)
    await db.flush()

    attendance_id = new_attendance.id

    await db.commit()

    result = await db.execute(
        select(StudentAttendance)
        .where(StudentAttendance.id == attendance_id)
    )

    attendance_data = result.scalar_one()

    return GenericResponse(
        success=True,
        message="Student attendance marked successfully",
        data=StudentAttendanceResponse(
            id=attendance_data.id,
            date=attendance_data.date,
            status=attendance_data.status,
            check_in=attendance_data.check_in,
            check_out=attendance_data.check_out,
            remarks=attendance_data.remarks,
            student_id=attendance_data.student_id,
        )
    )