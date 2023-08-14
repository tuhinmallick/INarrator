from typing import List
from narrator.email.email import IEmail
from abc import ABC, abstractmethod




class IUser(ABC):
    email:IEmail = None

    def __init__(self, email:IEmail):
        self.email = email

    @abstractmethod
    def authenticate(self):
        pass
    @abstractmethod
    def read_last_email(self) -> str:
        pass
    @abstractmethod
    def read_latest_emails(self) -> str:
        pass
    @abstractmethod
    def summarize_latest_emails(self) -> str:
        pass

class User(IUser):

    def __init__(self,email:IEmail):
        self.email = email
    
    def authenticate(self):
        self.email.authenticate()
    
    def read_last_email(self) -> str:
        pass
    
    def read_latest_emails(self) -> List[str]:
        return self.email.get_latest_emails()

    def summarize_latest_emails(self) -> str:
        pass

