from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    nick = Column(String, index=True, unique=True)
    hash_password = Column(String)
    is_premium = Column(Boolean, default=False)
    experience = Column(Integer, default=0)

class FollowedFriends(Base):
    __tablename__ = 'followed_friends'
    id = Column(Integer, primary_key=True, index=True)
    following_user_id = Column(Integer, ForeignKey('users.id'))
    followed_user_id = Column(Integer, ForeignKey('users.id'))

class Ships(Base):
    __tablename__ = 'ships'
    id = Column(Integer, primary_key=True, index=True)
    tier = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

class Journey(Base):
    __tablename__ = 'journeys'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ship_id = Column(Integer, ForeignKey('ships.id'))
    duration = Column(Integer)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_type = Column(Integer, default=0)
    experience_to_get = Column(Integer)

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
