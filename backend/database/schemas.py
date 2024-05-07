from pydantic import BaseModel,Field,Json
from typing import Optional,Union
from fastapi import UploadFile, Form, File
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

# Token

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


## User

class UserBase(BaseModel):
    username: str
    password: str


class User(UserBase):
    __tablename__ = "user"
    id: Optional[int] = Field(primary_key=True)


class UserCreate(UserBase):
   email: str

class UserResponse(User):
   pass

## Document

class DocumentBase(BaseModel):
    title: str 
    owner_id: int 

class Document(DocumentBase):
    __tablename__ = "document"
    id: Optional[int] = Field(primary_key=True)


class UploadedFile(BaseModel):
    url: str
    path: str
    size: int
    files: List[str]
    saved: bool
    file_id: str
    filename: str
    uploaded_at: datetime
    content_path: Optional[str]
    content_type: str
    upload_storage: str

class DocumentCreate(DocumentBase):
    content: UploadedFile