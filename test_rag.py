import sys
sys.stdout.reconfigure(encoding="utf-8")

from backend.app.services.ingestion import load_document
from backend.app.services.chunking import split_documents
from backend.app.services.embedding import create_embeddings
from backend.app.services.vector_store import create_vector_store
from backend.app.services.retrieval import retrieve_documents
from backend.app.services.rag import build_context, build_prompt, generate_answer
from backend.app.services.llm import create_llm


# 1. Load document
documents = load_document(
    "data/documents/facebook policy.pdf"
)

print("Number of pages:", len(documents))


# 2. Split document into chunks
chunks = split_documents(documents)

print("Number of chunks:", len(chunks))


# 3. Create embeddings
embeddings = create_embeddings()


# 4. Create vector store
vector_store = create_vector_store(
    chunks,
    embeddings
)

print("Vector store created!")


# 5. User query
query = "How are board members selected and appointed?"


# 6. Retrieve relevant documents
results = retrieve_documents(
    vector_store,
    query
)

print("Number of retrieved documents:", len(results))


# 7. Build context
context = build_context(results)


# 8. Build prompt
prompt = build_prompt(
    context,
    query
)


# 9. Print final prompt
print("\n========== FINAL PROMPT ==========\n")
print(prompt)


llm = create_llm()

answer = generate_answer(llm, prompt)

print("\n========== FINAL ANSWER ==========\n")
print(answer)