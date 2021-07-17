from typing import List, Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    # rating: Optional[int] = None
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int

    class Config:
        orm_mode = True
