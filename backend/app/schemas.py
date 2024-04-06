from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# For users

class UserBase(BaseModel):
    nick: str
    is_premium: Optional[bool] = False
    experience: Optional[int] = 0

class UserId(BaseModel):
    user_id: int

class UserExperience(BaseModel):
    user_id: int
    experience: int

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

# For friends

class FriendsBase(BaseModel):
    following_user_id: int
    followed_user_id: int

class Friends(FriendsBase):
    id: int
    class Config:
        orm_mode = True

# For journey

class Journey(BaseModel):
    user_id: int
    duration: int
    start_date: datetime = datetime.now()


class JourneyResponseModel(BaseModel):
    id: int
    user_id: int
    duration: int
    start_date: datetime

    class Config:
        orm_mode = True

# Score board

class ScoreboardItem(BaseModel):
    user_id: int
    experience: int
    
    class Config:
        orm_mode = True

# For ships

class ShipBase(BaseModel):
    user_id: int
    tier: int

class Ship(ShipBase):
    id: int

    class Config:
        orm_mode = True
