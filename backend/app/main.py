from fastapi import FastAPI, Request
from models import Base
from database import SessionLocal, engine
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
import time
from routes.users import route as users_route
from routes.tasks import route as tasks_route
from routes.auth import route as auth_route

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_app() -> FastAPI:
    """
    инициалиализация app, 
    """
    app = FastAPI(
        title="TrackMe api",
        version="0.1.1",
        redoc=None
    )
    app.include_router(users_route)
    app.include_router(tasks_route)
    app.include_router(auth_route)
    return app

app: FastAPI = create_app()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response