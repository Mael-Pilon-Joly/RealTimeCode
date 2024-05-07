import os

from database import models,schemas
from sqlalchemy.orm import Session
from sqlalchemy_file import File
from fastapi import UploadFile

def get_document(db, id: int):
    db_document = db.query(models.Document).filter(models.Document.id == id).first()
    file_obj = File(content=db_document.content, filename=db_document.title)
    return { "title":db_document.title, "owner_id":db_document.owner_id, "content": file_obj}

def get_document_by_title(db: Session, title:str):
     return db.query(models.Document).filter(models.Document.title == title).first()

def get_documents_by_user(db: Session, owner_id:int, skip:int=0, limit:int=100):
    return db.query(models.Document).filter(models.Document.owner_id == owner_id).offset(skip).limit(limit).all()

def create_document(db: Session, document:schemas.DocumentCreate, file:UploadFile):
    file_obj = File(content=file.file.read(), filename=document.title)  

    db_document = models.Document(title=document.title,
                                   content=file_obj,
                                   owner_id=document.owner_id)

    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return { "title":db_document.title, "owner_id":db_document.owner_id, "content": file_obj}