from __future__ import print_function

import os.path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime
import json

class GoogleCalendar:
    
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.file_path = "token.json" #might need to change
        self.service = None
    
    def renew_google_token(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.file_path):
            creds = Credentials.from_authorized_user_file(self.file_path, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0) #might need to change credentials.json name
            # Save the credentials for the next run
            with open(self.file_path, 'w') as token:
                token.write(creds.to_json())
        
        return creds
    
    def get_google_token(self):
        self.renew_google_token()
        
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data["token"]
    
    def set_google_calendar(self, event):
        creds = self.renew_google_token()
        service = build('calendar', 'v3', credentials=creds)
        self.service = service
        self.service.events().insert(calendarId='primary', body=event).execute()
    
    def delete_event(self):
        return self.service.events().delete(calendarId='primary').execute()
    

