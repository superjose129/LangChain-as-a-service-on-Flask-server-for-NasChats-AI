"""
This file uses stored vectors in Pinecone and use them as context when sending questions to LLMs - openai in this case
"""

import os
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
import pinecone

# from consts import INDEX_NAME
INDEX_NAME="amotions-data-index"

load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENVIRONMENT_REGION")
pinecone.init(api_key=api_key, environment=environment)


def run_llm(query):
    # embedd the query as a new text and return a vector(embeddings) for it
    embeddings = OpenAIEmbeddings()

    # search for similar vectors in the vectorstore Pinecone and return these vectors(docsearch)
    docsearch = Pinecone.from_existing_index(
        index_name=INDEX_NAME, embedding=embeddings
    )

    # chain the returned vectors with the query and send them to llm - query + context (which is the vectors here)
    chat = ChatOpenAI(verbose=True, temperature=0)
    qa = RetrievalQA.from_chain_type(
        llm=chat,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
    )  # qa chain

    return qa({"query": query})

if __name__ == "__main__":
    # pass
    print("please wait, we working on answering your question ...")
    print(run_llm("I want to tell my employee that she needs to improve her communication. Can you tell me exactly how to say it?"))