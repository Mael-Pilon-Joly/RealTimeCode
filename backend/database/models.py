from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.ext.declarative  import declarative_base
from sqlalchemy import Column,Integer
from sqlalchemy.types import LargeBinary
from sqlalchemy_file import FileField

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id= Column(Integer, primary_key=True)
    username= Column(String(16), index=True)
    password= Column(String(100), index=True)
    email= Column(String(64), index=True)

class Document(Base):
    __tablename__ = "document"
    id= Column(Integer, primary_key=True)
    title= Column(String(64), index=True)
    content= Column(FileField)
    owner_id=Column(Integer, ForeignKey("user.id"))