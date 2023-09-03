from __future__ import annotations
from abc import ABC, abstractmethod
from inarrator.email.message import IMessage
from langchain.chains import LLMChain

class ISummarizer(ABC):
    def __init__(self, api_token: str, model_name: str):
        self.chain = self.load_chain(api_token, model_name)

    @classmethod
    @abstractmethod
    def load_chain(self, api_token: str, model_name: str) -> LLMChain:
        """"""
        pass

    def summarize(self, message: IMessage) -> str:
        """"""
        pass
