from fastapi import APIRouter
from ..crud import *
from ..models import *
from  ..schemas import *
from ..database import SessionLocal, engine
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from ..config import Settings

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


route = APIRouter(
    prefix="/tasks",
    tags=["tasks endpoints"]
)

@route.get("/all_tasks", response_model=list[Task]|NotAuthToken)
def get_tasks(secret: str, db: Session = Depends(get_db)):
    if secret == Settings.secret_token:
        return get_tasks(db)
    return {"status": "Invalid secret code"}


@route.post("/create_task", response_model=Task|NotAuthToken)
def create_task(secret: str, task: TaskCreate, db: Session = Depends(get_db)):
    if secret == Settings.secret_token:
        return create_task(db, task)
    return {"status": "Invalid secret code"}



