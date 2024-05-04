from pydantic import BaseModel,Field
from typing import Optional

class UserBase(BaseModel):
    username: str
    password: str
    email: str


class User(UserBase):
    __tablename__ = "user"
    id: Optional[int] = Field(primary_key=True)


class UserCreate(UserBase):
    pass

class UserResponse(User):
   pass