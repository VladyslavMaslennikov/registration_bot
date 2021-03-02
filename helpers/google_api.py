from datetime import datetime, timedelta

import os.path
import pickle

import googleapiclient.errors
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from data.config import GOOGLE_CALENDAR_ID as cal_id

import helpers.date_functions as date_func

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']

CREDENTIALS_FILE = 'data/secret.json'


def get_calendar_service():
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            credentials = flow.run_local_server(port=8080)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    service = build('calendar', 'v3', credentials=credentials)
    return service


def find_all_events_for_day(date: datetime):
    service = get_calendar_service()
    lower = datetime(date.year, date.month, date.day, 10).isoformat() + "Z"
    upper = datetime(date.year, date.month, date.day, 22).isoformat() + "Z"
    events = service.events().list(
        calendarId=cal_id, timeMin=lower, timeMax=upper,
        maxResults=10, singleEvents=True,  # events from 10:00 to 22:00, max events 10
        orderBy='startTime').execute()
    items = events.get('items', [])
    all_busy_hours = []
    for item in items:
        start = item["start"]["dateTime"]
        end = item["end"]["dateTime"]
        all_busy_hours = all_busy_hours + date_func.check_busy_hours(start, end)
    print(f"Busy hours for the day: {all_busy_hours}")
    available_hours = date_func.return_available_hours(all_busy_hours)
    print(f"Available hours are: {available_hours}")
    return available_hours


def create_new_event(date: datetime, name: str, phone: str):
    service = get_calendar_service()
    current_date = datetime(date.year, date.month, date.day, date.hour)
    start = current_date.isoformat()
    end = (current_date + timedelta(hours=1)).isoformat()

    event_result = service.events().insert(calendarId=cal_id,
                                           body={
                                               "summary": f"Запись на сеанс: {name}",
                                               "description": f"Номер телефона: {phone}",
                                               "start": {
                                                   "dateTime": start, "timeZone": 'Europe/Kiev'
                                               },
                                               "end": {
                                                   "dateTime": end, "timeZone": 'Europe/Kiev'
                                               },
                                           }
                                           ).execute()
    return event_result


def delete_event(date: str):
    register_date = date_func.get_date_from_string(date)
    service = get_calendar_service()

    service = get_calendar_service()
    lower = datetime(register_date.year, register_date.month, register_date.day, 10).isoformat() + "Z"
    upper = datetime(register_date.year, register_date.month, register_date.day, 22).isoformat() + "Z"
    events = service.events().list(
        calendarId=cal_id, timeMin=lower, timeMax=upper,
        maxResults=1, singleEvents=True,  # events from 10:00 to 22:00, max events 10
        orderBy='startTime').execute()
    items = events.get('items', [])
    for item in items:
        event_id = item["id"]
        try:
            service.events().delete(
                calendarId=cal_id,
                eventId=event_id,
            ).execute()
        except googleapiclient.errors.HttpError:
            print("Failed to delete event")
        print("Event deleted")
