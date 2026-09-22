import sys

sys.stdout.reconfigure(encoding="utf-8")
from backend.app.services.ingestion import load_document
from backend.app.services.chunking import split_documents
from backend.app.services.embedding import create_embeddings
from backend.app.services.vector_store import create_vector_store
from backend.app.services.retrieval import retrieve_documents


file_path = "data/documents/facebook policy.pdf"

documents = load_document(file_path)

chunks = split_documents(documents)

embeddings = create_embeddings()

vector_store = create_vector_store(
    chunks,
    embeddings
)

query = "How are board members selected and appointed?"

results = retrieve_documents(
    vector_store,
    query
)

print("Number of results:", len(results))

for result in results:
    print("\n--- RESULT ---")
    print(result.page_content[:500])
    print("Metadata:", result.metadata)