from common.database import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import Integer,String,Boolean,Time,ForeignKey

class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subject: Mapped[str] = mapped_column(String(30))
    qualification: Mapped[str] = mapped_column(String(100)) #highest degree

    user = relationship("User", back_populates="teacher")
    student_link = relationship("StudentTeacher",back_populates="linked_teacher")
    teacher_attendance = relationship("TeacherAttendance",back_populates="teacher")

    def __repr__(self):
        return f"teacher(id={self.id}, name={self.name})"#dunder method used for debugging

