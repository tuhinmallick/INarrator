from typing import List,Any
from abc import ABC, abstractmethod
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
import os


class IEmail(ABC):
    service:Any = None
    @abstractmethod
    def authenticate(self):
        pass
    @abstractmethod
    def get_last_email(self) -> str:
        pass
    @abstractmethod
    def get_latest_emails(self) -> List[str]:
        pass
    @abstractmethod
    def get_last_n_emails(self, n:int) -> List[str]:
        pass


class Gmail(IEmail):
    service:Any = None
    def authenticate(self):
        """Authenicate the Email Client given User Authorization"""
        creds = None
        if os.path.exists('token.json'): # TODO: This will go to a storage system to save user tokens
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'narrator/email/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token: # TODO: Should be stored  somewhere
            token.write(creds.to_json())
        
        flow = InstalledAppFlow.from_client_secrets_file(
            'narrator/email/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        try:
            # Call the Gmail API
            self.service = build('gmail', 'v1', credentials=creds)
            results = self.service.users().labels().list(userId='me').execute()
        except HttpError as error:
            print(f'An error occurred: {error}')
    
    def get_last_email(self) -> str:
        pass
    
    def get_latest_emails(self) -> List[str]:
        results = self.service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages',[])
        return messages
    
    def get_last_n_emails(self, n:int) -> List[str]:
        pass


