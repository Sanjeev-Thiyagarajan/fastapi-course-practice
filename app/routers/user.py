from fastapi import APIRouter, Depends, status, HTTPException, Response

from .. import schemas, models, utils, database
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)


@router.post('/', response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    hashedPassword = utils.hash(user.password)
    user.password = hashedPassword
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user
