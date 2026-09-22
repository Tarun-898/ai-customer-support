from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from backend.app.services.embedding import create_embeddings
from backend.app.services.vector_store import load_vector_store
from backend.app.services.retrieval import retrieve_documents
from backend.app.services.rag import (
    build_context,
    build_prompt,
    generate_answer
)
from backend.app.services.llm import create_llm
from backend.app.services.router import classify_query

router = APIRouter()


class ChatRequest(BaseModel):

    company_id: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    query: str = Field(
        ...,
        min_length=3,
        max_length=500
    )

    @field_validator("company_id", "query")
    @classmethod
    def validate_text(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value


embeddings = create_embeddings()
vector_store = load_vector_store(embeddings)
llm = create_llm()

@router.post("/chat")
def chat(request: ChatRequest):

    try:

        route = classify_query(request.query)

        if route == "greeting":
            return {
                "company_id": request.company_id,
                "question": request.query,
                "answer": "Hello! How can I help you today?"
            }

        results = retrieve_documents(
            vector_store,
            request.query,
            request.company_id
        )

        if not results:
            return {
                "company_id": request.company_id,
                "question": request.query,
                "answer": "I don't have enough information to answer that."
            }

        context = build_context(results)

        prompt = build_prompt(
            context,
            request.query
        )

        answer = generate_answer(
            llm,
            prompt
        )

        return {
            "company_id": request.company_id,
            "question": request.query,
            "answer": answer
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to process your request right now"
        )