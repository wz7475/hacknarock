from fastapi import Depends
from sqlalchemy.orm import Session

from app import schemas as schemas, models as models
from app.database import get_db
from app.main import app


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(nick=user.nick, is_premium=user.is_premium, experience=user.experience)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
