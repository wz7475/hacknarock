from fastapi import APIRouter, HTTPException, Cookie, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.database import get_db
import app.models as models
import app.schemas as schemas
from app.cfg import SECRET_KEY, HASHING_ALGORITHM
from jose import jwt

journey_router = APIRouter(prefix="/journeys")


MAP_STATUS_TO_TEXT = {
    0: "Ended Successfully",
    1: "Ended by user",
    2: "Ended by storm"
}


@journey_router.get("/")
def get_all_journeys(db: Session = Depends(get_db)):
    return db.query(models.Journey).all()


@journey_router.post("/", response_model=schemas.JourneyResponseModel)
def create_journey(journey: schemas.Journey, jwt_cookie: str = Cookie(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(jwt_cookie, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    user_id = decoded_jwt.get('user_id')
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    ship = db.query(models.Ships).filter(models.Ships.id == journey.ship_id).first()
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")

    db_journey = models.Journey(user_id=user_id, ship_id=journey.ship_id, duration=journey.duration, start_date=journey.start_date)
    db.add(db_journey)
    db.commit()
    db.refresh(db_journey)
    return db_journey


@journey_router.post('/end_journey')
def end_journey(end_journey: schemas.EndJourney, jwt_cookie: str = Cookie(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(jwt_cookie, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    if end_journey.end_type not in range(3):
        raise HTTPException(status_code=400, detail="Journey end-type has to be in range 0 and 2")
    journey = db.query(models.Journey).filter(models.Journey.id == end_journey.id and models.Journey.user_id == decoded_jwt.get('user_id')).first()
    journey.end_type = end_journey.end_type
    db.commit()
    return JSONResponse(content={"message": f"Journey with id: '{end_journey.id}' has ended with status: '{MAP_STATUS_TO_TEXT[end_journey.end_type]}'"})


@journey_router.get('/get_user_journeys', response_model=schemas.JourneyResponseModel)
def get_ids_of_user_journeys(jwt_cookie: str = Cookie(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(jwt_cookie, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    user_id = decoded_jwt.get('user_id')
    return db.query(models.Journey).filter(models.Journey.user_id == user_id).all()


@journey_router.post("/{journey_id}")
def delete_journey(journey_id: int, db: Session = Depends(get_db)):
    db.query(models.Journey).filter(models.Journey.id == journey_id).delete()
    db.commit()
    return {"message": "Journey deleted successfully"}
