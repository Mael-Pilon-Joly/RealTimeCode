import os

from dotenv import dotenv_values
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status,Form,UploadFile
from sqlalchemy.orm import Session
from controllers import utils
from utils import documents
from database import models, schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta, timezone
from pydantic import Json
from typing import Annotated
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager

# Configure Storage
os.makedirs("./upload_dir/attachment", 0o777, exist_ok=True)
container = LocalStorageDriver("./upload_dir").get_container("attachment")
StorageManager.add_storage("default", container)

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

## user
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

## document
@app.get("/documents/{id}", response_model=schemas.DocumentCreate)
def get_document_by_id(id: int, db:Session=Depends(get_db)):
    document = documents.get_document(db,id)
    return document

@app.get("/documents/users/{id}", response_model=schemas.Document)
def get_documents_by_user(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    _documents = documents.get_documents_by_user(db,skip=skip,limit=limit)
    return _documents

@app.post("/documents/",response_model=schemas.DocumentCreate)
def post_document(content: UploadFile, document:schemas.DocumentBase= Depends(), db:Session=Depends(get_db)):
    db_document = documents.get_document_by_title(db, title=document.title)
    if db_document:
        raise HTTPException(status_code=400, detail="Title already exist")
    return documents.create_document(db, document, content)