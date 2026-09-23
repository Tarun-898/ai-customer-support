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
from fastembed import TextEmbedding
from langchain_core.embeddings import Embeddings


class FastEmbed(Embeddings):

    def __init__(self):
        self.model = TextEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def embed_documents(self, texts):

        return list(
            self.model.embed(texts)
        )

    def embed_query(self, text):

        return list(
            self.model.embed([text])
        )[0]


def create_embeddings():

    return FastEmbed()

