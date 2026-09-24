# from langchain_chroma import Chroma

# def create_vector_store(chunks,embeddings):
#     vector_store=Chroma.from_documents(
#         documents=chunks,
#         embedding=embeddings,
#         persist_directory="chroma_db"
#     )
#     return vector_store


import os

import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma

load_dotenv()


def get_chroma_client():
    return chromadb.CloudClient(
        api_key=os.getenv("CHROMA_API_KEY"),
        tenant=os.getenv("CHROMA_TENANT"),
        database=os.getenv("CHROMA_DATABASE")
    )


def create_vector_store(chunks, embeddings):

    client = get_chroma_client()

    vector_store = Chroma(
        client=client,
        collection_name="customer_support",
        embedding_function=embeddings
    )

    vector_store.add_documents(chunks)

    return vector_store


def load_vector_store(embeddings):

    client = get_chroma_client()

    vector_store = Chroma(
        client=client,
        collection_name="customer_support",
        embedding_function=embeddings
    )

    return vector_store


def add_documents(vector_store, chunks, company_id):

    for chunk in chunks:
        chunk.metadata["company_id"] = company_id

    vector_store.add_documents(chunks)

    return vector_store