from typing import List,Any
from abc import ABC, abstractmethod
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from inarrator.email.message import Message

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
import os


class IEmail(ABC):
    service:Any = None
    @property
    def _type():
        "Type of Email API"
        pass
    
    @abstractmethod
    def authenticate(self, **kwargs:Any):
        """Authenticate the underlying EMAIL API to access user emails
        Args:
            kwargs: Key word argument needed to authenticate email API.
        """
        pass
    @abstractmethod
    def get_last_email(self) -> Message:
        """Get the latest received email from user inbox
        
        Returns:
            Email Message
        """
        pass
    @abstractmethod
    def get_latest_emails(self, **kwargs:Any) -> List[Message]:
        """Get the latest unread emails from user inbox
        Args:
            kwargs: Keyword argument needed to get the latest emails
        
        Returns:
            List of Email Messages
        """
        pass
    @abstractmethod
    def get_last_n_emails(self, n:int) -> List[Message]:
        """Get the last n received emails from user inbox
        Args:
            n: Number of last n emails

        Returns:
            Email Message
        """
        pass
    @abstractmethod
    def get_email(self, **kwargs) -> Message:
        """Get specific email from user inbox given filters
        
        Args:
            kwargs: Filters
        
        Returns:
            Email Message
        """
        pass
class Gmail(IEmail):
    service:Any = None
    
    @property
    def _type():
        return "Gmail"
    def authenticate(self, **kwargs:Any):
        """Authenicate the Email Client given User Authorization"""
        if "credentials_path" not in kwargs:
            raise ValueError("Need to provide Gmail API credential json file path")
        creds = None
        if os.path.exists('token.json'): # TODO: This will go to a storage system to save user tokens
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    kwargs.get("credentials_path"), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        try:
            # Call the Gmail API
            self.service = build('gmail', 'v1', credentials=creds)
            results = self.service.users().labels().list(userId='me').execute()
        except HttpError as error:
            print(f'An error occurred: {error}')
    
    def get_last_email(self) -> str:
        pass
    
    def get_latest_emails(self, **kwargs:Any) -> List[Message]:
        results = self.service.users().messages().list(userId="me", labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages',[])
        # Now get individual messages payload and format them
        for message_dict in messages:
            raw_message_payload = self.get_email(user_email = "me", gmail_id = message_dict.get('id'))
            print(raw_message_payload)
        return messages
    
    def get_last_n_emails(self, n:int) -> List[str]:
        pass

    def get_email(self, **kwargs:Any):        
        return self.service.users().messages().get(userId="me",id = kwargs.get('gmail_id')).execute()
