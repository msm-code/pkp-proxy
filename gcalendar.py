from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def make_service_oauth():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def make_service_serviceaccount():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    sa_file = 'credentials.json'
    creds = service_account.Credentials.from_service_account_file(sa_file, scopes=SCOPES)

    return build('calendar', 'v3', credentials=creds)


def train_added(service, train):
    try:
        return service.events().get(calendarId='msm2e4d534d@gmail.com', eventId=train.eventid).execute() is not None
    except HttpError as e:
        # 404 not found, new train
        return False


def add_train(service, ticket):
    print(ticket.starttime)
    event = {
        'id': ticket.eventid,
        'summary': f'Train {ticket.start} - {ticket.end}',
        'description': f'Ticket {ticket.ticket_id}. Trains: {ticket.trains}. {ticket.start} - {ticket.end}',
        'start': {
            'dateTime': ticket.starttime,
            'timeZone': 'Europe/Warsaw',
        },
        'end': {
            'dateTime': ticket.endtime,
            'timeZone': 'Europe/Warsaw',
        },
    }
    print(event)

    event = service.events().insert(calendarId='msm2e4d534d@gmail.com', body=event).execute()
    print(event)
    print('Event created: %s' % (event.get('htmlLink')))
