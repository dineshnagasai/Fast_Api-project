from sqlalchemy.orm import  Mapped, mapped_column,relationship
from sqlalchemy import Integer,String,Boolean,ForeignKey
from common.database import Base
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from modules.user.models import User

class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    age : Mapped[int] = mapped_column(Integer)
    department: Mapped[str] = mapped_column(String(30))

    user = relationship("User", back_populates="student")
    parent_link = relationship("StudentParent",back_populates="linked_student")
    student_attendance = relationship("StudentAttendance",back_populates="student")
    teacher_link = relationship("StudentTeacher",back_populates="linked_student")

    def __repr__(self):
        return f"User(id={self.id}, name={self.user_id})"

class StudentParent(Base): #association model
    __tablename__ = "student_parent"

    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True) #composite primary key
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"), primary_key=True)
    relationship_type: Mapped[str] = mapped_column(String(20))

    linked_student = relationship("Student", back_populates="parent_link")
    linked_parent = relationship("Parent", back_populates="student_link")

class StudentTeacher(Base):
    __tablename__ = "student_teacher"

    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"), primary_key=True)

    linked_student = relationship("Student", back_populates="teacher_link")
    linked_teacher = relationship("Teacher", back_populates="student_link")