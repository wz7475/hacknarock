from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session

from app import schemas as schemas, models as models
from app.database import get_db


user_router = APIRouter()

@user_router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = models.User(nick=user.nick, is_premium=user.is_premium, experience=user.experience)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@user_router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.id == user_id).first()


@user_router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, db: Session = Depends(get_db)):
    return db.query(models.User).offset(skip).all()


@user_router.post("/users/buy_premium")
def buy_premium(user: schemas.UserId, db: Session = Depends(get_db)):
    found_user = db.query(models.User).filter(models.User.id == user.user_id).first()
    if found_user.is_premium:
        return {"message": f"User with id: {user.user_id} is already premium"}
    found_user.is_premium = True
    db.commit()
    return {"message": f"User with id: {user.user_id} is now premium"}


@user_router.post("/users/follow_user", response_model=schemas.Friends)
def follow_user(users: schemas.FriendsBase, db: Session = Depends(get_db)):
    if users.following_user_id == users.followed_user_id:
        raise HTTPException(status_code=400, detail="Cannot follow self")

    followed_already = db.query(models.FollowedFriends).filter(models.FollowedFriends.followed_user_id == users.followed_user_id and models.FollowedFriends.following_user_id == users.following_user_id).first()
    if followed_already:
        return followed_already

    
    friends = models.FollowedFriends(following_user_id=users.following_user_id, followed_user_id=users.followed_user_id)
    db.add(friends)
    db.commit()
    db.refresh(friends)
    return friends


@user_router.get("/users/list_followed/{user_id}", response_model=list[int])
def list_followed_users(user_id: int, db: Session = Depends(get_db)):
    followed = db.query(models.FollowedFriends).filter(models.FollowedFriends.following_user_id == user_id).all()
    return set([follower.followed_user_id for follower in followed])


@user_router.get("/users/list_following/{user_id}", response_model=list[int])
def list_following_users(user_id: int, db: Session = Depends(get_db)):
    followers = db.query(models.FollowedFriends).filter(models.FollowedFriends.followed_user_id == user_id).all()
    return set([follower.following_user_id for follower in followers])
