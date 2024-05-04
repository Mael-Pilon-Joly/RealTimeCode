from dotenv import dotenv_values
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from controllers import utils
from database import models, schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta, timezone

secrets = dotenv_values(".env")
engine = create_engine("mysql+pymysql://"+secrets["mysql_username"]+":"+secrets["mysql_password"]+"@localhost:3306/realtimecode", echo=True)

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

@app.get("/users/", response_model=list[schemas.User])
def get_users(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    users = utils.get_users(db,skip=skip,limit=limit)
    return users

@app.post("/users/",response_model=schemas.User)
def post_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    db_user = utils.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return utils.create_user(db=db,user=user)

@app.post("/login")
async def login_for_access_token(
   user:schemas.UserBase, db:Session=Depends(get_db)
) -> schemas.Token:
    user = utils.authenticate_user(user, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
