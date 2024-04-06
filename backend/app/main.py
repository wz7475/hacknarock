from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(nick=user.nick, is_premium=user.is_premium, experience=user.experience)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Add more CRUD operations for User and other models...
