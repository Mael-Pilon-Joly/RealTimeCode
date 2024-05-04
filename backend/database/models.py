from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.ext.declarative  import declarative_base
from sqlalchemy import Column,Integer

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id= Column(Integer, primary_key=True)
    username= Column(String(16), index=True)
    password= Column(String(32), index=True)
    email= Column(String(64), index=True)