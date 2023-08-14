from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain


llm = HuggingFaceHub(repo_id="google/pegasus-large", huggingfacehub_api_token="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")
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
docs = loader.load()
chain = load_summarize_chain(llm, chain_type="stuff")
print(chain.run(docs))