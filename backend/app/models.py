from sqlalchemy import DateTime,ForeignKey, Integer, String, Text,func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class BlogGeneration(Base):
    __tablename__ = "blog_generations"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    thread_id : Mapped[str] = mapped_column(String(255),unique=True,nullable=False)
    prompt : Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    content : Mapped[str] = mapped_column(Text,nullable=True)
    pdf_path : Mapped[str] = mapped_column(String(255),nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    
    