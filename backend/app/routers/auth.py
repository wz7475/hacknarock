from fastapi import APIRouter, Header
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Depends, Request, Cookie
from fastapi.security import OAuth2PasswordBearer
import requests
from jose import jwt
from dotenv import load_dotenv
import os

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
from jose import jwt

load_dotenv()
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = "http://127.0.0.1:8080/google-auth"
SCOPE = "https://www.googleapis.com/auth/calendar"


@auth_router.get("/login/google/")
async def login_google(authorization: str = Cookie()):
    res = RedirectResponse(
        f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope={SCOPE}")
    res.set_cookie(key="jwt", value=authorization)
    return res
    # return {
    #     "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope={SCOPE}"
    # }


def get_dummy_event(year=2024, month=4, day=28):
    if month < 10:
        month = f"0{month}"
    if day < 10:
        day = f"0{day}"
    event = {
        'summary': 'event from api',
        'start': {
            'dateTime': f'{year}-{month}-{day}T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': f'{year}-{month}-{day}T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return event

def create_event(access_token: str):
    # craete event
    event_creation_url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.post(event_creation_url, headers=headers, json=get_dummy_event(day=10))


@auth_router.get("/google-auth")
async def auth_google(code: str, request: Request):
    jwt_token = request.cookies.get("jwt")
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    # save in redis     jwt: access_token
    redis = {}
    redis[jwt_token] = access_token


    res = RedirectResponse("http://172.98.2.193:3000/app")
    return res

@auth_router.get("/token/")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])
