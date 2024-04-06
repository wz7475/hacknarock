from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import schemas as schemas, models as models
from app.database import get_db


user_router = APIRouter(prefix="/users")

@user_router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = models.User(nick=user.nick, is_premium=user.is_premium, experience=user.experience)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@user_router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.id == user_id).first()


@user_router.post("/grant_experience")
def grant_experience(data: schemas.UserExperience, db: Session = Depends(get_db)):
    if data.experience < 0:
        raise HTTPException(status_code=400, detail="Cannot grant negative experience")
    
    user = db.query(models.User).filter(models.User.id == data.user_id).first()
    user.experience += data.experience
    db.commit()
    return JSONResponse(content={"message": f"User with id: {data.user_id} had been granted: {data.experience} experience and now has total: {user.experience}"})


@user_router.get("/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@user_router.post("/buy_premium")
def buy_premium(user: schemas.UserId, db: Session = Depends(get_db)):
    found_user = db.query(models.User).filter(models.User.id == user.user_id).first()
    if found_user.is_premium:
        return JSONResponse(content={"message": f"User with id: {user.user_id} is already premium"})
    found_user.is_premium = True
    db.commit()
    return JSONResponse(content={"message": f"User with id: {user.user_id} is now premium"})


@user_router.post("/follow_user", response_model=schemas.Friends)
def follow_user(users: schemas.FriendsBase, db: Session = Depends(get_db)):
    if users.following_user_id == users.followed_user_id:
        raise HTTPException(status_code=400, detail="Cannot follow self")

    followed_already = db.query(models.FollowedFriends).filter(models.FollowedFriends.followed_user_id == users.followed_user_id and models.FollowedFriends.following_user_id == users.following_user_id).first()
    
    if followed_already is None:
        raise HTTPException(status_code=400, detail="User you are trying to follow doesn't exist")
    
    if followed_already:
        return followed_already

    
    friends = models.FollowedFriends(following_user_id=users.following_user_id, followed_user_id=users.followed_user_id)
    db.add(friends)
    db.commit()
    db.refresh(friends)
    return friends


@user_router.get("/list_followed/{user_id}", response_model=list[schemas.User])
def list_followed_users(user_id: int, db: Session = Depends(get_db)):
    followed = db.query(models.FollowedFriends).filter(models.FollowedFriends.following_user_id == user_id).all()
    ids_of_followed_users = set([follower.followed_user_id for follower in followed])    
    return [db.query(models.User).filter(models.User.id == id_of_followed_user).first() for id_of_followed_user in ids_of_followed_users]


@user_router.get("/list_following/{user_id}", response_model=list[schemas.User])
def list_following_users(user_id: int, db: Session = Depends(get_db)):
    followers = db.query(models.FollowedFriends).filter(models.FollowedFriends.followed_user_id == user_id).all()
    ids_of_followers = set([follower.following_user_id for follower in followers])
    return [db.query(models.User).filter(models.User.id == id_of_follower).first() for id_of_follower in ids_of_followers]


@user_router.get("/scoreboard/")
def get_scoreboard(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    output_raw = [{"user_id": user.id, "experience": user.experience} for user in users]
    return sorted(output_raw, key=lambda x: x.get('experience'), reverse=True)