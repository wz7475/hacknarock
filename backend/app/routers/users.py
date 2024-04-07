from fastapi import APIRouter, HTTPException, Response, Cookie, Depends, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import schemas as schemas, models as models
from app.database import get_db
from app.cfg import ACCESS_TOKEN_EXPIRE_MINUTES, HASHING_ALGORITHM, SECRET_KEY
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext

from jose import jwt

user_router = APIRouter(prefix="/users")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(username, password, db):
    user = db.query(models.User).filter(models.User.nick == username).first()
    if user is None:
        raise HTTPException(status_code=400, detail=f"User with given nick: '{username}' doesn't exist")
    hashed_password = pwd_context.hash(password, salt="a"*21 + "e")
    if user.hash_password == hashed_password:
        return user
    raise HTTPException(status_code=401, detail="Incorrect password")


def create_access_token(data: dict, expires_delta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASHING_ALGORITHM)
    return encoded_jwt


@user_router.post("/register")
def register(user: schemas.RegisterUser, response: Response, db: Session = Depends(get_db)) -> schemas.Jwt:
    hashed_password = pwd_context.hash(user.password, salt="a"*21 + "e")
    
    nick_exists = db.query(models.User).filter(models.User.nick == user.nick).first()
    if nick_exists is not None:
        raise HTTPException(status_code=400, detail=f"User with nick: '{user.nick}' already exists")
    
    db_user = models.User(nick=user.nick, is_premium=user.is_premium, experience=user.experience, hash_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_nick": db_user.nick, "user_id": db_user.id}, expires_delta=access_token_expires
    )
    response.set_cookie(key='jwt_cookie', value=access_token)
    return schemas.Jwt(jwt=access_token)

@user_router.post("/login")
def login_for_access_token(data: schemas.UserLogin, response: Response, db: Session = Depends(get_db)) -> schemas.Jwt:
    try:
        user = authenticate_user(data.nick, data.password, db)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_nick": user.nick, "user_id": user.id}, expires_delta=access_token_expires
    )
    response.set_cookie(key='jwt_cookie', value=access_token)
    return schemas.Jwt(jwt=access_token)


@user_router.get("/user", response_model=schemas.User)
def read_user(jwt_cookie: str = Cookie(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(jwt_cookie, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    user_id = decoded_jwt.get('user_id')
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=400, detail="JWT expired")
    return user

@user_router.post("/grant_experience")
def grant_experience(experience: schemas.UserExperience, jwt_cookie: str = Cookie(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(jwt_cookie, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    user_id = decoded_jwt.get('user_id')
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user.experience < 0:
        raise HTTPException(status_code=400, detail="Cannot grant negative experience")

    user.experience += experience.experience
    db.commit()
    return JSONResponse(content={"message": f"User with id: {user_id} had been granted: {experience.experience} experience and now has total: {user.experience}"})


@user_router.get("/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@user_router.post("/buy_premium")
def buy_premium(jwt_cookie: str = Cookie(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(jwt_cookie, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    user_id = decoded_jwt.get('user_id')
    found_user = db.query(models.User).filter(models.User.id == user_id).first()
    if found_user.is_premium:
        return JSONResponse(content={"message": f"User with id: {user_id} is already premium"})
    found_user.is_premium = True
    db.commit()
    return JSONResponse(content={"message": f"User with id: {user_id} is now premium"})


def get_user_id_by_nick(user_nick: str, db):
    user = db.query(models.User).filter(models.User.nick == user_nick).first()
    return user.id

@user_router.post("/follow_user", response_model=schemas.Friends)
def follow_user(user_to_be_followed: schemas.AddFriend, jwt_cookie: str = Cookie(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(jwt_cookie, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    user_id = decoded_jwt.get('user_id')
    
    user_self = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user_self.nick == user_to_be_followed.followed_user_nick:
        raise HTTPException(status_code=400, detail="Cannot follow self")

    check_if_followed_exists = db.query(models.User).filter(models.User.nick == user_to_be_followed.followed_user_nick).first()
    if check_if_followed_exists is None:
        raise HTTPException(status_code=400, detail="User you are trying to follow doesn't exist")
    
    followed_id = get_user_id_by_nick(user_to_be_followed.followed_user_nick, db)
    
    followed_already = db.query(models.FollowedFriends).filter(models.FollowedFriends.followed_user_id == followed_id and models.FollowedFriends.following_user_id == user_id).first()
    
    if followed_already is not None:
        raise HTTPException(status_code=400, detail="You are already following this user")

    friends = models.FollowedFriends(following_user_id=user_id, followed_user_id=followed_id)
    db.add(friends)
    db.commit()
    db.refresh(friends)
    return friends


@user_router.get("/list_followed", response_model=list[schemas.User])
def list_followed_users(jwt_cookie: str = Cookie(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(jwt_cookie, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    user_id = decoded_jwt.get('user_id')
    followed = db.query(models.FollowedFriends).filter(models.FollowedFriends.following_user_id == user_id).all()
    ids_of_followed_users = set([follower.followed_user_id for follower in followed])    
    return [db.query(models.User).filter(models.User.id == id_of_followed_user).first() for id_of_followed_user in ids_of_followed_users]


@user_router.get("/list_following", response_model=list[schemas.User])
def list_following_users(jwt_cookie: str = Cookie(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(jwt_cookie, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    user_id = decoded_jwt.get('user_id')
    followers = db.query(models.FollowedFriends).filter(models.FollowedFriends.followed_user_id == user_id).all()
    ids_of_followers = set([follower.following_user_id for follower in followers])
    return [db.query(models.User).filter(models.User.id == id_of_follower).first() for id_of_follower in ids_of_followers]


@user_router.get("/scoreboard/")
def get_scoreboard(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    output_raw = [{"user_id": user.id, "experience": user.experience} for user in users]
    return sorted(output_raw, key=lambda x: x.get('experience'), reverse=True)
