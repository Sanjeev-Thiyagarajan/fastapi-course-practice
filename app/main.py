import enum
from fastapi import FastAPI, Request, Response, status, HTTPException, Depends
from typing import Optional, List
from fastapi.param_functions import Body
from random import randrange
from .routers import post, user, auth

from pydantic import BaseModel

from sqlalchemy.orm import Session

from . import models, schemas, utils, config
from .database import engine, SessionLocal, get_db

my_posts = [{"id": 1, "title": "my first post", "content": "random text"},
            {"id": 2, "title": "my second post", "content": "I like dogs"}]

print(config.settings.database_hostname)


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
# fjsdf


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None
    published: bool = True


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
# @app.post("/")
# async def my_post(request: schemas.PostBase, db: Session = Depends(get_db)):
#     new_post = models.Post(title=request.title)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post


@app.get("/")
async def root():
    return {"message": "hello there"}
