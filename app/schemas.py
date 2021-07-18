from typing import List, Optional

from pydantic import BaseModel
# from sqlalchemy.sql.sqltypes import Boolean


class PostBase(BaseModel):
    title: str
    content: str
    # rating: Optional[int] = None
    published: bool = True


class PostCreate(PostBase):
    pass


class UserBase(BaseModel):
    email: str
    id: int

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    owner: UserBase

    class Config():
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str

    class Config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
