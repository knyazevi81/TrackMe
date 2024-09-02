# авторизация
from fastapi import APIRouter
import crud, models, schemas
from database import SessionLocal, engine
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from routes.jwt_utils import create_access_token

route = APIRouter(
    prefix="/auth",
    tags=["authentication services"]
)

def authenticate_user(email: str, password: str, db: Session):
    pass


@route.get("")
def get_jwt_token():
    data = {"sub": "wfwefew@mail.ru"}
    return create_access_token(data)