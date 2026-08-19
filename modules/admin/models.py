from common.database import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import Integer,String,Boolean,Time,ForeignKey

class Admin(Base):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),unique=True)
    designation: Mapped[str] = mapped_column(String(100))
    user = relationship("User",back_populates="admin")

    def __repr__(self):
        return f"Admin(id={self.id}, designation={self.designation})"