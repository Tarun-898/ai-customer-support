import sys

sys.stdout.reconfigure(encoding="utf-8")

from backend.app.services.ingestion import load_document

file_path = "data/documents/facebook policy.pdf"

documents = load_document(file_path)

print("Number of pages:", len(documents))

for doc in documents[-2:]:
    print("\n--- PAGE ---")
    print(doc.page_content[:1000])