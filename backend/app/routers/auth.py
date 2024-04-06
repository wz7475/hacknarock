from fastapi import APIRouter
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
import requests
from jose import jwt
from dotenv import load_dotenv
import os

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = "http://127.0.0.1:8080/google-auth"
SCOPE = "https://www.googleapis.com/auth/calendar"

@auth_router.get("/login/google/")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope={SCOPE}"
    }

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

@auth_router.get("/google-auth")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    event_creation_url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    r = requests.post("https://oauth2.googleapis.com/token", data=data)
    credentials = r.text
    access_token = response.json().get("access_token")

    # craete event
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    with open("token.txt", "w") as f:
        f.write(access_token)
    response = requests.post(event_creation_url, headers=headers, json=get_dummy_event(day=10))
    event_response = response.json()
    if response.status_code == 200:
        return {"message": "Event created", "event_id": event_response['id']}
    else:
        return {"message": "Failed to create event", "error": event_response}


@auth_router.get("/token/")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])
