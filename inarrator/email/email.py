"""Module to Get Emails Data using respective API(s)."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any, Sequence

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from inarrator.email.message import GmailMessage, IMessage


class IEmail(ABC):
    """Abstract Class for Email Instances."""

    service: Any = None
    """Main API Python Client"""

    @property
    def _type(self) -> str:
        """Type of Email API."""
        return "IEmail"

    @abstractmethod
    def authenticate(self, **kwargs: Any) -> None:
        """Authenticate the underlying EMAIL API to access user emails.

        Args:
        ----
            kwargs: Key word argument needed to authenticate email API.
        """
        pass

    @abstractmethod
    def get_latest_emails(self, **kwargs: Any) -> Sequence[IMessage]:
        """Get the latest unread emails from user inbox.

        Args:
        ----
            kwargs: Keyword argument needed to filter out the latest emails.

        Returns:
        -------
            List of Email Messages
        """
        pass

    @abstractmethod
    def get_email(self, **kwargs: Any) -> IMessage:
        """Get specific email from user inbox given a unique identifier for the email.

        Args:
        ----
            kwargs: Keyword Argument for the unique id.

        Returns:
        -------
            Email Message
        """
        pass


class Gmail(IEmail):
    service: Any = None

    @property
    def _type(self) -> str:
        return "Gmail"

    def authenticate(self, **kwargs: Any) -> None:
        if "credentials_path" not in kwargs:
            raise ValueError("Need to provide Gmail API credential json file path")
        creds = None
        if os.path.exists(
            "token.json"
        ):  # TODO: This will go to a storage system to save user tokens
            creds = Credentials.from_authorized_user_file("token.json", kwargs.get("gmail_scope"))
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    kwargs.get("credentials_path"), kwargs.get("gmail_scope")
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        try:
            # Call the Gmail API
            self.service = build("gmail", "v1", credentials=creds)
            self.service.users().labels().list(userId="me").execute()
        except HttpError as error:
            print(f"An error occurred: {error}")

    def get_latest_emails(self, **kwargs: Any) -> Sequence[IMessage]:
        results = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                includeSpamTrash=False,
                maxResults=kwargs.get("gmail_max_emails", 10),
                labelIds=["INBOX"],
                q=kwargs.get("gmail_filters", "is:unread"),
            )
            .execute()
        )
        messages = results.get("messages", [])
        messages_list = []
        # Now get individual messages payload and format them
        for message_dict in messages:
            raw_message_payload = self.get_email(user_email="me", gmail_id=message_dict.get("id"))
            message = GmailMessage.parse_message(raw_message_payload=raw_message_payload)
            if message:
                messages_list.append(message)
        return messages_list

    def get_email(self, **kwargs: Any) -> Any:
        return self.service.users().messages().get(userId="me", id=kwargs.get("gmail_id")).execute()


class OutLook(IEmail):
    pass