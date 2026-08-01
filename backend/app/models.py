from sqlalchemy import DateTime,ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username : Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email : Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password : Mapped[str] = mapped_column(String(255))
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class BlogGeneration(Base):
    __tablename__ = "blog_generations"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    topic : Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    content : Mapped[str] = mapped_column(Text,nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    