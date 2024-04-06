import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import SCOPES, CREDENTIALS_PATH, TOKEN_PATH


# If modifying these scopes, delete the file token.json.

def authorize():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds


def get_service(creds):
    return build("calendar", "v3", credentials=creds)


def get_events(service):
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return events_result.get("items", [])


def print_events(events):
    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])


def create_event(service, event):
    service.events().insert(calendarId='primary', body=event).execute()


def get_dummy_event(year=2024, month=4, day=28):
    if month < 10:
        month = f"0{month}"
    if day < 10:
        day = f"0{day}"
    event = {
        'summary': 'event from backend',
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


def main():
    creds = authorize()
    service = get_service(creds)

    event = get_dummy_event(day=8)
    create_event(service, event)

    events = get_events(service)
    print_events(events)


if __name__ == "__main__":
    main()
