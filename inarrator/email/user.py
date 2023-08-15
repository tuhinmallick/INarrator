from typing import List,Any,Dict
from abc import ABC, abstractmethod


from inarrator.email.email import IEmail
from inarrator.email.message import Message
from inarrator.exceptions



class IUser(ABC):
    def __init__(self, emails:List[IEmail]):
        self.emails = emails

    @abstractmethod
    def authenticate(self):
        """Authentication of each email API for the given user"""
        pass
    @abstractmethod
    def read_last_email(self) -> Message:
        """Getting the latest email for the user"""
        pass
    @abstractmethod
    def read_latest_emails(self) -> Dict[str,List[Message]]:
        """Getting the latest unread emails from the user"""
        pass
    @abstractmethod
    def summarize_latest_emails(self) -> str:
        pass

class User(IUser):

    def __init__(self,emails:List[IEmail]):
        self.emails = emails
    
    def authenticate(self, **kwargs:Any):
        for email in self.emails:
            if not email.service:
                raise AuthenticationError(f"Authentication Error. Make sure following {email._type} API has not been authenticated")
    
    def read_last_email(self) -> Message:
        pass
    
    def read_latest_emails(self) -> Dict[str,List[Message]]:
        emails_dict = {}
        for email in self.emails:
            emails_dict[email._type] = email.get_latest_emails()
            
    def summarize_latest_emails(self) -> str:
        pass

