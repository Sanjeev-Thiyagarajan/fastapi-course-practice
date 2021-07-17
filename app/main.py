import enum
from fastapi import FastAPI, Request, Response, status, HTTPException, Depends
from typing import Optional
from fastapi.param_functions import Body
from random import randrange

from pydantic import BaseModel

from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, SessionLocal

my_posts = [{"id": 1, "title": "my first post", "content": "random text"},
            {"id": 2, "title": "my second post", "content": "I like dogs"}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
# fjsdf


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None
    published: bool = True


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.post("/")
async def my_post(request: schemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(title=request.title)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/")
async def root():
    return {"message": "hello there"}


@ app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return posts


@ app.post("/posts", status_code=status.HTTP_201_CREATED, )
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000)
    # my_posts.append(post_dict)
    # print(my_posts)

    # new_post = models.Post(title=post.title, content=post.content)
    print(post.dict())
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {new_post}


@app.get("/posts/{id}", )
async def get_post(id: int, response: Response, db: Session = Depends(get_db)):

    # post = find_post(id)
    # print(post)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with the id {id} is not available")

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the id {id} is not available")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id: int, db: Session = Depends(get_db)):

    # for idx, p in enumerate(my_posts):
    #     print(p)
    #     if p['id'] == id:
    #         del my_posts[idx]
    #         return Response(status_code=status.HTTP_204_NO_CONTENT)

    # index = find_index_post(id)
    # print(index)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} does not exist")
    # my_posts.pop(index)

    post = db.query(models.Post).filter(models.Post.id ==
                                        id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # index = find_index_post(id)
    # print(index)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} does not exist")

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict

    # print(post.dict())
    post = db.query(models.Post).filter(
        models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post.update({'title': 'hello'}, synchronize_session=False)
    print(post)
    db.commit()

    return "updated post"
