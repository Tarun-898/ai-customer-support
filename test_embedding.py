import sys

sys.stdout.reconfigure(encoding="utf-8")

from backend.app.services.ingestion import load_document
from backend.app.services.chunking import split_documents
from backend.app.services.embedding import create_embeddings


file_path = "data/documents/facebook policy.pdf"

documents = load_document(file_path)

chunks = split_documents(documents)

embeddings = create_embeddings()

vector = embeddings.embed_query(chunks[0].page_content)

print("Number of pages:", len(documents))
print("Number of chunks:", len(chunks))
print("Vector dimensions:", len(vector))
print("First 10 values:", vector[:10])