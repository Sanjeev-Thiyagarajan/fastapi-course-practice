from fastapi import FastAPI, Request
from typing import Optional
from fastapi.param_functions import Body
from random import randrange

from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None


app = FastAPI()


@ app.get("/")
async def root():
    return {"message": "Hello World"}


@ app.get("/posts")
async def get_posts():
    return {"data": "getting posts"}


@ app.post("/posts")
async def create_post(post: Post):
    post_dict = post.dict()
    # print(post.title)
    return {"data": post}
