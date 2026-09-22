# from langchain_chroma import Chroma

# def create_vector_store(chunks,embeddings):
#     vector_store=Chroma.from_documents(
#         documents=chunks,
#         embedding=embeddings,
#         persist_directory="chroma_db"
#     )
#     return vector_store


from langchain_chroma import Chroma


def create_vector_store(chunks, embeddings):
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    return vector_store


def load_vector_store(embeddings):
    vector_store = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    return vector_store


def add_documents(vector_store, chunks, company_id):

    for chunk in chunks:
        chunk.metadata["company_id"] = company_id

    vector_store.add_documents(chunks)

    return vector_store