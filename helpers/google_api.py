from datetime import datetime, timedelta

import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from data.config import GOOGLE_CALENDAR_NAME as cal_name, GOOGLE_CALENDAR_ID as cal_id
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
    calendar = service.calendars().get(calendarId=cal_id).execute()  # finding calendar
    print(calendar['summary'])
    lower = datetime(date.year, date.month, date.day, 10).isoformat('T') + "Z"
    upper = datetime(date.year, date.month, date.day, 22).isoformat('T') + "Z"
    events = service.events().list(
        calendarId=cal_id, timeMin=lower, timeMax=upper,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events_dict = events.get('items', [])
    print(events_dict)

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])


def create_new_event(date: datetime):
    service = get_calendar_service()
    current_date = datetime(date.year, date.month, date.day, date.hour)
    start = current_date.isoformat()
    end = (current_date + timedelta(hours=1)).isoformat()

    event_result = service.events().insert(calendarId=cal_id,
                                           body={
                                               "summary": cal_name,
                                               "description": 'Fake registration',
                                               "start": {
                                                   "dateTime": start, "timeZone": 'EET'
                                               },
                                               "end": {
                                                   "dateTime": end, "timeZone": 'EET'
                                               },
                                           }
                                           ).execute()
