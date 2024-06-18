# app/models.py
from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    disabled = Column(Boolean, default=False)
    scopes = Column(String, default="regular_user")  # admin, moderator, regular_user

    user_api_services = relationship("UserAPIService", back_populates="user")


class APIService(Base):
    __tablename__ = "api_services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String)
    port = Column(Integer)
    documentation = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    user_api_services = relationship("UserAPIService", back_populates="api_service")


class UserAPIService(Base):
    __tablename__ = "user_api_services"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    api_service_id = Column(Integer, ForeignKey("api_services.id"), primary_key=True)
    status = Column(String)  # pending, approved, rejected
    access = Column(Boolean, default=True)
    request_per_action = Column(Integer, default=120)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    exp_date = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc) + timedelta(days=30)
    )

    user = relationship("User", back_populates="user_api_services")
    api_service = relationship("APIService", back_populates="user_api_services")


class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    api_service_id = Column(Integer, ForeignKey("api_services.id"))
    action = Column(String)  # e.g., "requested access", "approved access"
    timestamp = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    detail = Column(String)
