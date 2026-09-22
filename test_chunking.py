import sys
sys.stdout.reconfigure(encoding="utf-8")

from backend.app.services.ingestion import load_document
from backend.app.services.chunking import split_documents

file_path = "data/documents/facebook policy.pdf"

documents = load_document(file_path)

chunks = split_documents(documents)

print("Number of pages:", len(documents))
print("Number of chunks:", len(chunks))

for chunk in chunks[:3]:
    print("\n--- CHUNK ---")
    print(chunk.page_content[:500])
    print("Metadata:", chunk.metadata)