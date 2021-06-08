from fastapi import FastAPI, Request, Response, status, HTTPException
from typing import Optional
from fastapi.param_functions import Body
from random import randrange

from pydantic import BaseModel

my_posts = [{"id": 1, "title": "my first post", "content": "random text"},
            {"id": 2, "title": "my second post", "content": "I like dogs"}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


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


@ app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000)
    my_posts.append(post_dict)
    print(my_posts)
    return {"data": post}


@app.get("/posts/{id}")
async def get_post(id: int, response: Response):

    post = find_post(id)
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the id {id} is not available")
    return {"detail": post}


# @app.delete("/posts/{id}")
# async def delete_posts(id: int):
#     for idx, p in enumerate(my_posts):
#         print(p)
#         if p['id'] == id:
#             del my_posts[idx]
#             return
