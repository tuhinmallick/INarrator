
from typing import Any
from dataclasses import dataclass

@dataclass
class Message:
    id: int
    to: str
    fro: str
    raw_attachments: Any
    raw_payload: Any

    def payload(self, raw_payload) -> str:
        return raw_payload