from pydantic import BaseModel,Field
from typing import Optional,Union

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

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