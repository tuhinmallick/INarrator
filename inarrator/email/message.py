from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Union

import html2text

from inarrator.utils import base64url_decode


@dataclass
class IMessage(ABC):
    to: str
    fro: str
    subject: str
    body: str

    @classmethod
    @abstractmethod
    def parse_message(cls, **kwargs: Any) -> Union[IMessage, None]:
        """Parse the Raw Message payload and create a message instance.

        Args:
        ----
            kwargs: Message Payload Keyword Argument

        Returns:
        -------
            IMessage Instance

        """
        pass


@dataclass
class GmailMessage(IMessage):
    to: str
    fro: str
    subject: str
    body: str

    @classmethod
    def parse_message(cls, **kwargs: Any) -> Union[IMessage, None]:
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        raw_payload = kwargs.get("raw_message_payload", {})
        if not raw_payload:
            raise ValueError(
                "In order parse Gmail Email Payload you need to provide raw_message_payload"
            )
        payload = raw_payload.get("payload")
        headers = payload.get("headers")
        body = payload.get("body").get("data")
        if not body:
            return None
        headers_dict = {"To": "", "From": "", "Subject": ""}
        for header in headers:
            if header.get("name") == "From":
                headers_dict["From"] = header.get("value")
            elif header.get("name") == "To":
                headers_dict["To"] = header.get("value")
            elif header.get("Subject") == "Subject":
                headers_dict["Subject"] = header.get("value")

        return cls(
            to=headers_dict.get("To", ""),
            fro=headers_dict.get("From", ""),
            subject=headers_dict.get("Subject", ""),
            body=h.handle(base64url_decode(body)),
        )


@dataclass
class OutlookMessage(IMessage):
    to: str
    fro: str
    subject: str
    body: str

    @classmethod
    def parse_message(cls, **kwargs: Any) -> Union[IMessage, None]:
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        raw_payload = kwargs.get("raw_message_payload", {})
        if not raw_payload:
            raise ValueError(
                "In order parse Outlook Email Payload you need to provide raw_message_payload"
            )
        subject = raw_payload["subject"]
        message_body = h.handle(raw_payload["body"].get("content"))
        fro = raw_payload.get("from").get("emailAddress").get("address")
        to = ";".join(
            [email.get("emailAddress").get("address") for email in raw_payload.get("toRecipients")]
        )
        return cls(to=to, fro=fro, subject=subject, body=message_body)
