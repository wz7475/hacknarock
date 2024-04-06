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

# Define similar schemas for other models...
