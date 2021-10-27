from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def make_service():
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


def train_added(service, train):
    return service.events().get(calendarId='primary', eventId=train.eventid).execute() is not None


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

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))



if __name__ == '__main__':
    main()
