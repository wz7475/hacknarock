import os
import json
import requests
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import JSONResponse, RedirectResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

app = FastAPI()
app.credentials = None

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]
SCOPE = "https://www.googleapis.com/auth/calendar"

#event data format can be found here https://developers.google.com/calendar/api/guides/create-events
@app.post("/create_event")
async def create_event(event: dict):
    credentials_info = app.credentials
    if not credentials_info:
        raise HTTPException(status_code=401, detail="Please authenticate first using the oauth2callback endpoint.")
    # Convert the stored credentials from string to dictionary
    credentials_dict = json.loads(credentials_info)
    headers = {
        "Authorization": f"Bearer {credentials_dict['access_token']}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    event_creation_url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    try:
        response = requests.post(event_creation_url, headers=headers, json=event)
        event_response = response.json()
        if response.status_code == 200:
            return {"message": "Event created", "event_id": event_response['id']}
        else:
            return {"message": "Failed to create event", "error": event_response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/oauth2callback")
async def oauth2callback(request: Request, code: str = None):
    if not code:
        auth_uri = (
            "https://accounts.google.com/o/oauth2/v2/auth?response_type=code"
            "&client_id={}&redirect_uri={}&scope={}".format(CLIENT_ID, REDIRECT_URI, SCOPE)
        )
        return auth_uri
    else:
        data = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        r = requests.post("https://oauth2.googleapis.com/token", data=data)
        app.credentials = r.text
        response = JSONResponse(content="Successfully authenticated. You can now use the API to create events.")
        return response

@app.get('/clear_credentials')
async def clear_session(response: Response):
    app.credentials = None
    return "User credentials cleared."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)