from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    nick: str
    is_premium: Optional[bool] = False

class UserCreate(UserBase):
    experience: int

class User(UserBase):
    id: int
    class Config:
        orm_mode = True


class Journey(BaseModel):
    user_id: int
    duration: int
    # start_date: Optional[datetime] = datetime.now()
    start_date: datetime = datetime.now()


class JourneyResponseModel(BaseModel):
    id: int
    user_id: int
    duration: int
    start_date: datetime

    class Config:
        orm_mode = True