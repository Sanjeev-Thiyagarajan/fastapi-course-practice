from fastapi import FastAPI, Request
from typing import Optional
from fastapi.param_functions import Body
from random import randrange

from pydantic import BaseModel

my_posts = [{"id": 1, "title": "my first post", "content": "random text"},
            {"id": 2, "title": "my second post", "content": "I like dogs"}]


class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None


app = FastAPI()


@ app.get("/")
async def root():
    return {"message": "hello there"}


@ app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@ app.post("/posts")
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000)
    my_posts.append(post_dict)
    print(my_posts)
    return {"data": post}
