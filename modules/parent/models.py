from common.database import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import Integer,String,Boolean,Time,ForeignKey
from modules.user.models import User

class Parent(Base):
    __tablename__ = "parent"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),unique=True)
    occupation: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(100))

    user = relationship("User", back_populates="parent")
    student_link = relationship("StudentParent",back_populates="linked_parent")

    def __repr__(self):
        return f"Parent(id={self.id}, name={self.name})"
