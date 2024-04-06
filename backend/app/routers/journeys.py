from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Journey as JourneyModel
from app.schemas import Journey as JourneySchema
from app.schemas import JourneyResponseModel

journey_router = APIRouter()


@journey_router.get("/journeys/{user_id}")
def get_all_journeys(user_id: int, db: Session = Depends(get_db)):
    return db.query(JourneyModel).filter(JourneyModel.user_id == user_id).all()


@journey_router.post("/journeys/", response_model=JourneyResponseModel)
def create_journey(journey: JourneySchema, db: Session = Depends(get_db)):
    db_journey = JourneyModel(user_id=journey.user_id, duration=journey.duration)
    db.add(db_journey)
    db.commit()
    db.refresh(db_journey)
    return db_journey

@journey_router.post("/journeys/{journey_id}")
def delete_journey(journey_id: int, db: Session = Depends(get_db)):
    db.query(JourneyModel).filter(JourneyModel.id == journey_id).delete()
    db.commit()
    return {"message": "Journey deleted successfully"}
