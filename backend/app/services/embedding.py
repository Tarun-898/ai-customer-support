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


from langchain_huggingface import HuggingFaceEmbeddings


_embeddings = None


def create_embeddings():
    global _embeddings

    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    return _embeddings