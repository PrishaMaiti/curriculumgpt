import os
import streamlit as st
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain

# os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ['OPENAI_API_KEY'] = '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'

# Set persist directory
persist_directory = 'db'

business_loader = DirectoryLoader('./docs/business/', glob="*.pdf")
engr_loader = DirectoryLoader('./docs/engr/', glob="*.pdf")

business_docs = business_loader.load()
engr_docs = engr_loader.load()

embeddings = OpenAIEmbeddings()
text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=8)

# Split documents and generate embeddings
business_docs_split = text_splitter.split_documents(business_docs)
engr_docs_split = text_splitter.split_documents(engr_docs)

# Create Chroma instances and persist embeddings
business_docs = Chroma.from_documents(business_docs_split, embeddings, persist_directory=os.path.join(persist_directory, 'business'))
business_docs.persist()

engr_docs = Chroma.from_documents(engr_docs_split, embeddings, persist_directory=os.path.join(persist_directory, 'engr'))
engr_docs.persist()
