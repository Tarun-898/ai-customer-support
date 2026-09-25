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


COLLECTION_NAME = "customer_support"


def get_chroma_client():

    client = chromadb.CloudClient(
        api_key=os.getenv("CHROMA_API_KEY"),
        tenant=os.getenv("CHROMA_TENANT"),
        database=os.getenv("CHROMA_DATABASE")
    )

    return client


def create_vector_store(chunks, embeddings):

    client = get_chroma_client()

    vector_store = Chroma(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings
    )

    vector_store.add_documents(chunks)

    return vector_store


def load_vector_store(embeddings):

    client = get_chroma_client()

    vector_store = Chroma(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings
    )

    return vector_store


def add_documents(vector_store, chunks):

    vector_store.add_documents(chunks)

    return vector_store


def delete_document(vector_store, document_id):

    client = get_chroma_client()

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    collection.delete(
        where={
            "document_id": document_id
        }
    )

    return True


def get_document_metadata(document_id):

    client = get_chroma_client()

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    result = collection.get(
        where={
            "document_id": document_id
        },
        limit=1
    )

    if not result["metadatas"]:
        return None

    return result["metadatas"][0]


def get_company_documents(company_id):

    client = get_chroma_client()

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    result = collection.get(
        where={
            "company_id": company_id
        },
        include=["metadatas"]
    )

    return result