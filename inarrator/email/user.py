from abc import ABC, abstractmethod
from typing import Any, Dict, List, Sequence

from inarrator.email.email import IEmail
from inarrator.email.message import IMessage
from inarrator.exceptions import AuthenticationError


class IUser(ABC):
    def __init__(self, emails: List[IEmail]):
        self.emails = emails

    @abstractmethod
    def authenticate(self) -> None:
        """Authentication of each email API for the given user."""
        pass

    @abstractmethod
    def read_latest_emails(self) -> Dict[str, Sequence[IMessage]]:
        """Getting the latest unread emails from the user.

        Args:
        ----
            kwargs: Keyword Argument to filter out the latest emails

        Returns:
        -------
            A dictionary which consist of emails provider and messages from each email provider
        """
        pass

    @abstractmethod
    def summarize_latest_emails(self) -> str:
        pass


class User(IUser):
    def __init__(self, emails: List[IEmail]):
        self.emails = emails

    def authenticate(self) -> None:
        for email in self.emails:
            if not email.service:
                raise AuthenticationError(
                    f"""Authentication Error.
                    Make sure following {email._type} API has not been authenticated
                    """
                )

    def read_latest_emails(self, **kwargs: Any) -> Dict[str, Sequence[IMessage]]:
        emails_dict = {}
        for email in self.emails:
            emails_dict[email._type] = email.get_latest_emails(**kwargs)
        return emails_dict

    def summarize_latest_emails(self) -> str:
        return ""
