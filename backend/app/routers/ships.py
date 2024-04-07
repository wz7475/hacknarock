from fastapi import APIRouter, HTTPException, Cookie, Depends, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.cfg import SECRET_KEY, HASHING_ALGORITHM
from jose import jwt

from app import schemas as schemas, models as models
from app.database import get_db


ship_router = APIRouter(prefix="/ships")


@ship_router.get('/', response_model=list[schemas.Ship])
def get_ships(db: Session = Depends(get_db)):
    return db.query(models.Ships).all()


@ship_router.post('/add_ship', response_model=schemas.Ship)
def add_ship_to_user(data: schemas.ShipBase, jwt_cookie: str = Cookie(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(jwt_cookie, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    user_id = decoded_jwt.get('user_id')
    if data.tier not in range(5):
        raise HTTPException(status_code=400, detail="Ship tier has to be an integer between 1 and 5")
    
    ship = models.Ships(user_id=user_id, tier=data.tier)
    db.add(ship)
    db.commit()
    db.refresh(ship)
    return ship


@ship_router.get('/get_self_ships', response_model=list[schemas.Ship])
def get_ships_for_user(jwt_cookie: str = Cookie(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(jwt_cookie, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    user_id = decoded_jwt.get('user_id')
    return db.query(models.Ships).filter(models.Ships.user_id == user_id).all()


@ship_router.get('/get_other_users_ships', response_model=list[schemas.Ship])
def get_ships_by_user_id(other_user: schemas.UserId, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == other_user.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: '{other_user.user_id}' doesn't exist")
    return db.query(models.Ships).filter(models.Ships.user_id == other_user.user_id).all()


@ship_router.delete('/{ship_id}')
def remove_ship(ship_id: int, db: Session = Depends(get_db)):
    ship = db.query(models.Ships).filter(models.Ships.id == ship_id).first()
    db.delete(ship)
    db.commit()
    return JSONResponse(content={"message": f"Deleted ship with id: '{ship_id}'"})
