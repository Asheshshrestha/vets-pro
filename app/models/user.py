from datetime import datetime,timezone
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, ForeignKey, String, Integer, Boolean
from sqlalchemy.sql import func
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_on: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    created_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

class UserProfile(Base):
    __tablename__ = 'user_profile'
    
    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    first_name: Mapped[str] = mapped_column(String,nullable=True)
    middle_name: Mapped[str] = mapped_column(String,nullable=True)
    middle_name: Mapped[str] = mapped_column(String,nullable=True)
    email: Mapped[str] = mapped_column(String,nullable=True)
    profile_picture: Mapped[str] = mapped_column(String,nullable=True)
    country_code: Mapped[str] = mapped_column(String,nullable=True)
    phone_number: Mapped[str] = mapped_column(String,nullable=True)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_phone_number_verified: Mapped[bool] = mapped_column(Boolean, default=False)