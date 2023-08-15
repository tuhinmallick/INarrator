from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import WebBaseLoader
from langchain.llms import HuggingFaceHub

llm = HuggingFaceHub(repo_id="google/pegasus-large", huggingfacehub_api_token="")
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
docs = loader.load()
chain = load_summarize_chain(llm, chain_type="stuff")
print(chain.run(docs))
