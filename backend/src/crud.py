from sqlalchemy.orm import Session
import models
import schemas
from datetime import datetime

def get_users(db: Session, skip: int = 0, limit: int = 20) -> list[schemas.User]:
    """
    Вывод всех юзеров
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_exist(db: Session, tg_id: int):
    """
    Проверка на существаоние юзера
    """
    return db.query(models.User).filter(models.User.tg_id==tg_id).first()


def get_tasks(db: Session, skip_finished: bool = True):
    """
    Вывод всех существующих юзеров
     - флаг skip_finished отвечает за исполненные задачи, по умолчанию он True 
       то есть, выводит только исполненые задачи
    """
    if skip_finished:
        return db.query(models.Task).filter(models.Task.status==True).all()
    else:
        return db.query(models.Task).all()


def get_user_tasks(db: Session, users_id: int, skip_ready: bool = True):
    """
    Вывод задач конкретного юзера
    """
    if skip_ready:
        return db.query(models.Task).filter_by(
            models.Task.status==True,
            models.Task.user_id==users_id
        ).all()
    else:
        return db.query(models.Task).filter(
            models.Task.user_id==users_id
        ).all()
    

def create_task(db: Session, task: schemas.TaskCreate):
    """
    Функция для создания задачи для юзера
    """
    # FIX нужно добавить проверку на существование юзера
    # в ином случае задача будет создаваться для юзеров, которые не сущетсвует

    db_task = models.Task(
        **task.dict(),
        date=datetime.today().now()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        tg_id=user.tg_id,
        name=user.name,
        role=user.role,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def deactivate_user(db: Session, user_id):
    user = db.query(models.User).filter_by(id=user_id).first()
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


def activate_user(db: Session, user_id):
    user = db.query(models.User).filter_by(id=user_id).first()
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user


#def get_target(db: Session, url: str):
#    return db.query(models.Target).filter(models.Target.url == url).first()
#
#
#def get_targets(db: Session, skip: int = 0, limit: int = 100):
#    return db.query(models.Target).offset(skip).limit(limit).all()
#
#
#def create_target(db: Session, url_code: str, target: schemas.TargetCreate):
#    db_target = models.Target(
#        url = url_code,
#        redirect_by = target.redirect_by,
#        is_activate = True
#    )
#    db.add(db_target)
#    db.commit()
#    db.refresh(db_target)
#    return db_target
#
#def delete_target(db: Session, url_code: str):
#    target = db.query(models.Target).filter(models.Target.url == url_code).first()
#
#    if target:
#        target.is_activate = False
#
#        db.commit()
#        db.refresh(target)
#        return True
#    
#    return False
#
#
#
#def create_log(db: Session, log: schemas.LogCreate, target_id: int):
#    db_log = models.Log(**log.dict(), target_id=target_id)
#    db.add(db_log)
#    db.commit()
#    db.refresh(db_log)
#    return db_log



