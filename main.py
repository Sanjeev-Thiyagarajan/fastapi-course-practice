from fastapi import FastAPI, Request
from fastapi.param_functions import Body

from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def getPosts():
    return {"data": "getting posts"}


@app.post("/createposts")
async def create_post(post: Post):

    print(post.title)
    return {"data": post}
