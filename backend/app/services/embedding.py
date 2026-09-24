# from dotenv import load_dotenv
# from langchain_openai import OpenAIEmbeddings

# from dotenv import load_dotenv

# def create_embeddings():

#     embeddings = OpenAIEmbeddings(
#         model="text-embedding-3-small"
#     )

#     return embeddings




# from langchain_huggingface import HuggingFaceEmbeddings


# def create_embeddings():

#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )

#     return embeddings


import os
import requests

from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings

load_dotenv()


class JinaEmbeddings(Embeddings):

    def __init__(self):
        self.api_key = os.getenv("JINA_API_KEY")
        self.url = "https://api.jina.ai/v1/embeddings"
        self.model = "jina-embeddings-v3"

    def embed_documents(self, texts):

        response = requests.post(
            self.url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "input": texts
            }
        )

        response.raise_for_status()

        result = response.json()

        return [
            item["embedding"]
            for item in result["data"]
        ]

    def embed_query(self, text):

        response = requests.post(
            self.url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "input": [text]
            }
        )

        response.raise_for_status()

        result = response.json()

        return result["data"][0]["embedding"]


def create_embeddings():
    return JinaEmbeddings()

