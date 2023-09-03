from __future__ import annotations

from abc import ABC, abstractmethod
from inarrator.email.message import IMessage
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from inarrator.summarizer.prompt import EMAIL_PROMPT


class GPTModel(ABC):
    def __init__(self, api_token: str, model_name: str):
        self.chain = self.load_chain(api_token, model_name)

    @classmethod
    def load_chain(self, api_token: str, model_name: str) -> LLMChain:
        """"""

        return LLMChain(
            llm=ChatOpenAI(model_name = model_name, openai_api_key = api_token),
            prompt=PromptTemplate(
                template=EMAIL_PROMPT, input_variables=["fro", "to", "subject", "body"]
            ),
        )

    def summarize(self, message: IMessage) -> str:
        """"""
        return self.chain.predict(
                fro=message.fro,
                to=message.to,
                body=message.body,
                subject=message.subject,
            
        )