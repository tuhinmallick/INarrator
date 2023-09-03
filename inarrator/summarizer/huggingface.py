from __future__ import annotations

from abc import ABC, abstractmethod
from inarrator.email.message import IMessage
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from inarrator.summarizer.prompt import EMAIL_PROMPT


class HuggingFaceModel(ABC):
    def __init__(self, api_token: str, model_name: str):
        self.chain = self.load_chain(api_token, model_name)

    @classmethod
    def load_chain(self, api_token: str, model_name: str) -> LLMChain:
        """"""

        return LLMChain(
            llm=HuggingFaceHub(huggingfacehub_api_token=api_token, repo_id=model_name),
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
