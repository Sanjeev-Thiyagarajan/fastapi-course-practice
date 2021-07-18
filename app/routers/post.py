
from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/posts",
    tags=['Posts']

)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(database.get_db), get_current_User: schemas.UserLogin = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    print(posts)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db)):
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
    return new_post


@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(database.get_db)):

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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id: int, db: Session = Depends(database.get_db)):

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


@router.put("/{id}")
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db)):
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
