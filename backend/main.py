from dotenv import dotenv_values
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers import dbcrud
from database import models, schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware

secrets = dotenv_values(".env")
engine = create_engine("mysql+pymysql://"+secrets["mysql_username"]+":"+secrets["mysql_password"]+"@localhost:3306/realtimecode", echo=True)

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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
    users = dbcrud.get_users(db,skip=skip,limit=limit)
    return users

@app.post("/users/",response_model=schemas.User)
def post_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    db_user = dbcrud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return dbcrud.create_user(db=db,user=user)
