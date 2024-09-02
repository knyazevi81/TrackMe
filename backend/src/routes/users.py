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
    prefix="/users",
    tags=["users endpoints"]
)


@route.get("/all_users", response_model=list[schemas.User]|schemas.NotAuthToken)
def get_users(secret: str, db: Session = Depends(get_db)):
    if secret == Settings.secret_token:
        return crud.get_users(db)
    return {"status": "Invalid secret code"}


@route.post("/create_user", response_model=schemas.User|schemas.NotAuthToken)
def create_user(secret: str, user: schemas.UserCreate, db: Session = Depends(get_db)):
    # FIX при создании юзера с существующим tg_id вылетает ошибка, нужно ее покрыть
    if secret == Settings.secret_token:
        return crud.create_user(db, user)
    return {"status": "Invalid secret code"}


@route.post("/deactivate", response_model=schemas.User|schemas.NotAuthToken)
def deactivate_user(secret: str, user_id: int, db: Session = Depends(get_db)):
    if secret == Settings.secret_token:
        return crud.deactivate_user(db, user_id)
    return {"status": "Invalid secret code"}


@route.post("/activate", response_model=schemas.User|schemas.NotAuthToken)
def activate_user(secret: str, user_id: int, db: Session = Depends(get_db)):
    if secret == Settings.secret_token:
        return crud.activate_user(db, user_id)
    return {"status": "Invalid secret code"}


@route.get("/exist_user", response_model=schemas.ExistUser|schemas.NotAuthToken)
def get_exist_user(secret: str, tg_id: int, db: Session = Depends(get_db)):
    if secret == Settings.secret_token:
        status = True
        data = crud.get_user_exist(db, tg_id)
        if data == None: status = False
        return {
            "status": status,
            "user": data
        }
    return {"status": "Invalid secret code"}

#@route.post("/rerole", response_model=schemas.User)
#def 



