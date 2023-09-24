from inarrator.email.email import OutLook, Gmail
from inarrator.summarizer.huggingface import HuggingFaceModel
from inarrator.summarizer.gpt import GPTModel
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import WebBaseLoader
import os


gmail = Gmail()
gmail.authenticate(
    credentials_path="/home/mohtashimkhan/INarrator/gmail_credentials.json",
    gmail_scope=["https://www.googleapis.com/auth/gmail.readonly"],
)
emails = gmail.get_latest_emails(
        gmail_filters="from:(-noreply -no-reply) is:unread -category:social -category:promotions -unsubscribe",
        gmail_max_emails="30",
    )
os.environ['OPENAI_API_KEY'] = ''
model = GPTModel(model_name = 'gpt-3.5-turbo-16k',api_token='')
documents = []
for email in emails:
    documents.append(email)
print(model.summarize(documents[0]))



