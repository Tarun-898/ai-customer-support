from backend.app.services.ingestion import load_document
from backend.app.services.chunking import split_documents
from backend.app.services.embedding import create_embeddings
from backend.app.services.vector_store import create_vector_store


file_path = "data/documents/facebook policy.pdf"

documents = load_document(file_path)

chunks = split_documents(documents)

embeddings = create_embeddings()

vector_store = create_vector_store(
    chunks,
    embeddings
)

print("Number of pages:", len(documents))
print("Number of chunks:", len(chunks))
print("Vector store created successfully!")