from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import schemas as schemas, models as models
from app.database import get_db


ship_router = APIRouter(prefix="/ships")


@ship_router.get('/', response_model=list[schemas.Ship])
def get_ships(db: Session = Depends(get_db)):
    return db.query(models.Ships).all()


@ship_router.post('/add_ship', response_model=schemas.Ship)
def add_ship_to_user(data: schemas.ShipBase, db: Session = Depends(get_db)):
    if data.tier not in range(1, 6):
        raise HTTPException(status_code=400, detail="Ship tier has to be an integer between 1 and 5")
    
    ship = models.Ships(user_id=data.user_id, tier=data.tier)
    db.add(ship)
    db.commit()
    db.refresh(ship)
    return ship


@ship_router.get('/get_ships/{user_id}', response_model=list[schemas.Ship])
def get_ships_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Ships).filter(models.Ships.user_id == user_id).all()
