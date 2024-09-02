from pydantic import BaseModel
from enum import Enum
from datetime import date


class UserRole(str, Enum):
    user = "user"
    admin = "admin"
    main = "main"


class TaskBase(BaseModel):
    task_name: str
    message: str
    user_id: int
    status: bool


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    date: date


class UserBase(BaseModel):
    tg_id: int
    name: str
    role: UserRole
    

class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool = True
    tasks: list[Task] = []

    class Config:
        orm_mode = True


class ExistUser(BaseModel):
    status: bool
    user: User| None

class NotAuthToken(BaseModel):
    status: str