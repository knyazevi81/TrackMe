from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from enum import Enum
from .schemas import UserRole
import datetime


from .database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    tasks = relationship("Task", back_populates="task_id")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    task_name = Column(String, index=True)
    message = Column(String)
    status = Column(Boolean, default=True, nullable=False)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))

    task_id = relationship("User", back_populates="tasks")