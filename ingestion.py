"""
This file is to load documents and store them to the cloud vectorDB/vectoreStore Pinecone
"""

import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

# from consts import INDEX_NAME
INDEX_NAME="amotions-data-index"


load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENVIRONMENT_REGION")
pinecone.init(api_key=api_key, environment=environment)


def ingest_docs():
    # Load: loads our pdfs to langchain
    loader = PyPDFDirectoryLoader("dataPDFs/")
    print("Uploading pdfs ...")
    raw_documents = loader.load()
    print(f" Uploaded {len(raw_documents)} Documents")

    # Split Docs: splits the loaded documents into small chunks of text - Review chunking strategies
    # Usually we should have chunk size between 400 and 900 while passing 4-5 contexts with each question
    # We can experiement with different sizes and context counts as we improve our AI
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
    )
    documents = text_splitter.split_documents(documents=raw_documents)
    print(f" Documents splitted into {len(documents)} chunks")

    # Embedd and Store in Pinecone vectorStore: Convert text chunks into vectors and store them in vector DB
    print(f"Inserting {len(documents)} to Pinecone")
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents=documents, embedding=embeddings, index_name=INDEX_NAME)
    print(" Added to Pinecone vectorestore vectors")


if __name__ == "__main__":
    ingest_docs()
