from database import models,schemas
from sqlalchemy.orm import Session



def get_users(db: Session, skip:int=0, limit:int=100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user:schemas.UserCreate):
    db_user = models.User(username=user.username,
                          password=user.password,
                          email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()