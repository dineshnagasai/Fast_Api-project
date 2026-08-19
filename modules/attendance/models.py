from common.database import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import Integer,String,Boolean,Time,ForeignKey
from datetime import time

class StudentAttendance(Base):
    __tablename__ = "student_attendance"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    date: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20))
    check_in: Mapped[time] = mapped_column(Time)
    check_out: Mapped[time] = mapped_column(Time)
    remarks: Mapped[str] = mapped_column(String(100))
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))

    student = relationship("Student",back_populates="student_attendance")

    def __repr__(self):
        return f"attendance(id={self.id}, name={self.date})"

class TeacherAttendance(Base):
    __tablename__ = "teacher_attendance"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    date: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20))
    check_in: Mapped[time] = mapped_column(Time)
    check_out: Mapped[time] = mapped_column(Time)
    remarks: Mapped[str] = mapped_column(String(100))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))

    teacher = relationship("Teacher",back_populates="teacher_attendance")

    def __repr__(self):
        return f"attendance(id={self.id}, name={self.date})"
