from fastapi import APIRouter, HTTPException, Header, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Journey as JourneyModel
from app.schemas import Journey as JourneySchema
from app.schemas import JourneyResponseModel
from app.cfg import SECRET_KEY, HASHING_ALGORITHM
from jose import jwt

journey_router = APIRouter()


@journey_router.get("/journeys")
def get_all_journeys(authorization: str = Header(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(authorization, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    user_id = decoded_jwt.get('user_id')
    return db.query(JourneyModel).filter(JourneyModel.user_id == user_id).all()


@journey_router.post("/journeys", response_model=JourneyResponseModel)
def create_journey(journey: JourneySchema, authorization: str = Header(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(authorization, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    user_id = decoded_jwt.get('user_id')
    user = db.query(JourneyModel).filter(JourneyModel.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_journey = JourneyModel(user_id=user_id, duration=journey.duration, start_date=journey.start_date)
    db.add(db_journey)
    db.commit()
    db.refresh(db_journey)
    return db_journey


@journey_router.get('/get_user_journeys', response_model=JourneyResponseModel)
def get_ids_of_user_journeys(authorization: str = Header(), db: Session = Depends(get_db)):
    decoded_jwt = jwt.decode(authorization, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
    user_id = decoded_jwt.get('user_id')
    return db.query(JourneyModel).filter(JourneyModel.user_id == user_id).all()


@journey_router.post("/journeys/{journey_id}")
def delete_journey(journey_id: int, db: Session = Depends(get_db)):
    db.query(JourneyModel).filter(JourneyModel.id == journey_id).delete()
    db.commit()
    return {"message": "Journey deleted successfully"}
