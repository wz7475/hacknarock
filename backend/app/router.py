from fastapi import Depends
from sqlalchemy.orm import Session

from app import schemas as schemas, models as models
from app.database import get_db
from fastapi import APIRouter

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(nick=user.nick, is_premium=user.is_premium, experience=user.experience)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.id == user_id).first()


@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.User).offset(skip).limit(limit).all()
