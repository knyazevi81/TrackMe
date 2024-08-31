from fastapi import APIRouter
import crud, models, schemas
from database import SessionLocal, engine
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from config import Settings

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

@route.get("/all_tasks", response_model=list[schemas.Task]|schemas.NotAuthToken)
def get_tasks(secret: str, db: Session = Depends(get_db)):
    if secret == Settings.secret_token:
        return crud.get_tasks(db)
    return {"status": "Invalid secret code"}


@route.post("/create_task", response_model=schemas.Task|schemas.NotAuthToken)
def create_task(secret: str, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    if secret == Settings.secret_token:
        return crud.create_task(db, task)
    return {"status": "Invalid secret code"}



