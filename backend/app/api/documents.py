from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path

from backend.app.services.ingestion import load_document
from backend.app.services.chunking import split_documents
from backend.app.services.embedding import create_embeddings
from backend.app.services.vector_store import load_vector_store, add_documents


router = APIRouter()

UPLOAD_DIR = Path("data/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024

embeddings = create_embeddings()
vector_store = load_vector_store(embeddings)


@router.post("/documents")
async def upload_document(
    company_id: str = Form(...),
    file: UploadFile = File(...)
):

    company_id = company_id.strip()

    if not company_id:
        raise HTTPException(
            status_code=400,
            detail="Company ID cannot be empty"
        )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must be less than 10 MB"
        )

    file_path = UPLOAD_DIR / file.filename

    try:
        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        # Extract text
        documents = load_document(str(file_path))

        # Create chunks
        chunks = split_documents(documents)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the PDF"
            )

        # Add to vector database
        add_documents(
            vector_store,
            chunks,
            company_id
        )

    except HTTPException:
        if file_path.exists():
            file_path.unlink()
        raise

    except Exception as e:
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="Document processing failed"
        )

    return {
        "message": "Document uploaded and indexed successfully",
        "filename": file.filename,
        "company_id": company_id,
        "chunks": len(chunks)
    }