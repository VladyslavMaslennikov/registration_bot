from datetime import datetime
from dateutil.relativedelta import relativedelta
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'data/secrets.json'


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


def get_calendar_call_main():
    service = get_calendar_service()
    # Call the Calendar API
    print('Getting list of calendars')
    calendars_result = service.calendarList().list().execute()

    calendars = calendars_result.get('items', [])

    if not calendars:
        print('No calendars found.')
    for calendar in calendars:
        summary = calendar['summary']
        id_cal = calendar['id']
        primary = "Primary" if calendar.get('primary') else ""
        print("%s %s %s" % (summary, id_cal, primary))


def list_events():
    from data.config import GOOGLE_CALENDAR_ID as cal_id
    service = get_calendar_service()

    calendar = service.calendars().get(calendarId=cal_id).execute()  # finding calendar
    print(calendar['summary'])

    # Call the Calendar API
    now = datetime.today()
    following_month = now + relativedelta(months=1)
    t_min = now.isoformat('T') + "Z"
    t_max = following_month.isoformat('T') + "Z"
    print('Getting List of 10 events')
    events_result = service.events().list(
        calendarId=cal_id, timeMin=t_min, timeMax=t_max,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
