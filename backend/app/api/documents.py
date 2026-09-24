# from fastapi import APIRouter, UploadFile, File, Form, HTTPException
# from pathlib import Path

# from backend.app.services.ingestion import load_document
# from backend.app.services.chunking import split_documents
# from backend.app.services.embedding import create_embeddings
# from backend.app.services.vector_store import load_vector_store, add_documents


# router = APIRouter()

# UPLOAD_DIR = Path("data/documents")
# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# MAX_FILE_SIZE = 10 * 1024 * 1024

# embeddings = create_embeddings()
# vector_store = load_vector_store(embeddings)


# @router.post("/documents")
# async def upload_document(
#     company_id: str = Form(...),
#     file: UploadFile = File(...)
# ):

#     company_id = company_id.strip()

#     if not company_id:
#         raise HTTPException(
#             status_code=400,
#             detail="Company ID cannot be empty"
#         )

#     if not file.filename:
#         raise HTTPException(
#             status_code=400,
#             detail="Filename is required"
#         )

#     if not file.filename.lower().endswith(".pdf"):
#         raise HTTPException(
#             status_code=400,
#             detail="Only PDF files are supported"
#         )

#     file_content = await file.read()

#     if len(file_content) > MAX_FILE_SIZE:
#         raise HTTPException(
#             status_code=413,
#             detail="File size must be less than 10 MB"
#         )

#     file_path = UPLOAD_DIR / file.filename

#     try:
#         # Save file
#         with open(file_path, "wb") as buffer:
#             buffer.write(file_content)

#         # Extract text
#         documents = load_document(str(file_path))

#         # Create chunks
#         chunks = split_documents(documents)

#         if not chunks:
#             raise HTTPException(
#                 status_code=400,
#                 detail="No text could be extracted from the PDF"
#             )

#         # Add to vector database
#         add_documents(
#             vector_store,
#             chunks,
#             company_id
#         )

#     except HTTPException:
#         if file_path.exists():
#             file_path.unlink()
#         raise

#     except Exception as e:
#         if file_path.exists():
#             file_path.unlink()

#         raise HTTPException(
#             status_code=500,
#             detail="Document processing failed"
#         )

#     return {
#         "message": "Document uploaded and indexed successfully",
#         "filename": file.filename,
#         "company_id": company_id,
#         "chunks": len(chunks)
#     }




# from fastapi import APIRouter, UploadFile, File, Form, HTTPException
# from pathlib import Path

# from backend.app.services.ingestion import load_document
# from backend.app.services.chunking import split_documents
# from backend.app.services.embedding import create_embeddings
# from backend.app.services.vector_store import (
#     load_vector_store,
#     add_documents
# )


# router = APIRouter()


# # --------------------------------
# # Upload directory
# # --------------------------------

# UPLOAD_DIR = Path("data/documents")

# UPLOAD_DIR.mkdir(
#     parents=True,
#     exist_ok=True
# )


# # --------------------------------
# # Maximum file size: 10 MB
# # --------------------------------

# MAX_FILE_SIZE = 10 * 1024 * 1024


# # --------------------------------
# # Lazy-loaded vector store
# # --------------------------------

# vector_store = None


# def get_vector_store():

#     global vector_store

#     if vector_store is None:

#         embeddings = create_embeddings()

#         vector_store = load_vector_store(
#             embeddings
#         )

#     return vector_store


# @router.post("/documents")
# async def upload_document(
#     company_id: str = Form(...),
#     file: UploadFile = File(...)
# ):

#     # --------------------------------
#     # 1. Validate company ID
#     # --------------------------------

#     company_id = company_id.strip()

#     if not company_id:

#         raise HTTPException(
#             status_code=400,
#             detail="Company ID cannot be empty"
#         )


#     # --------------------------------
#     # 2. Validate filename
#     # --------------------------------

#     if not file.filename:

#         raise HTTPException(
#             status_code=400,
#             detail="Filename is required"
#         )


#     # --------------------------------
#     # 3. Validate file type
#     # --------------------------------

#     if not file.filename.lower().endswith(".pdf"):

#         raise HTTPException(
#             status_code=400,
#             detail="Only PDF files are supported"
#         )


#     # --------------------------------
#     # 4. Read uploaded file
#     # --------------------------------

#     file_content = await file.read()


#     # --------------------------------
#     # 5. Validate file size
#     # --------------------------------

#     if len(file_content) > MAX_FILE_SIZE:

#         raise HTTPException(
#             status_code=413,
#             detail="File size must be less than 10 MB"
#         )


#     # --------------------------------
#     # 6. Create file path
#     # --------------------------------

#     file_path = UPLOAD_DIR / file.filename


#     try:

#         # --------------------------------
#         # 7. Save PDF
#         # --------------------------------

#         with open(file_path, "wb") as buffer:

#             buffer.write(file_content)


#         # --------------------------------
#         # 8. Extract document text
#         # --------------------------------

#         documents = load_document(
#             str(file_path)
#         )


#         # --------------------------------
#         # 9. Split into chunks
#         # --------------------------------

#         chunks = split_documents(
#             documents
#         )


#         # --------------------------------
#         # 10. Check extracted chunks
#         # --------------------------------

#         if not chunks:

#             raise HTTPException(
#                 status_code=400,
#                 detail="No text could be extracted from the PDF"
#             )


#         # --------------------------------
#         # 11. Load vector store lazily
#         # --------------------------------

#         vector_store = get_vector_store()


#         # --------------------------------
#         # 12. Add documents to ChromaDB
#         # --------------------------------

#         add_documents(
#             vector_store,
#             chunks,
#             company_id
#         )


#     except HTTPException:

#         if file_path.exists():

#             file_path.unlink()

#         raise

#     except Exception as e:

#         import traceback

#         print("DOCUMENT PROCESSING ERROR:")
#         traceback.print_exc()

#         if file_path.exists():
#             file_path.unlink()

#         raise HTTPException(
#             status_code=500,
#             detail="Document processing failed"
#         )
#     # except Exception:

#         # if file_path.exists():

#         #     file_path.unlink()

#         # raise HTTPException(
#         #     status_code=500,
#         #     detail="Document processing failed"
#         # )


#     # --------------------------------
#     # 13. Success response
#     # --------------------------------

#     return {
#         "message": "Document uploaded and indexed successfully",
#         "filename": file.filename,
#         "company_id": company_id,
#         "chunks": len(chunks)
#     }




from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path

from backend.app.services.ingestion import load_document
from backend.app.services.chunking import split_documents
from backend.app.services.embedding import create_embeddings
from backend.app.services.vector_store import (
    load_vector_store,
    add_documents
)

router = APIRouter()

UPLOAD_DIR = Path("data/documents")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MAX_FILE_SIZE = 10 * 1024 * 1024

vector_store = None


def get_vector_store():
    global vector_store

    if vector_store is None:
        print("CREATING VECTOR STORE...")
        embeddings = create_embeddings()

        vector_store = load_vector_store(
            embeddings
        )

        print("VECTOR STORE READY")

    return vector_store


@router.post("/documents")
async def upload_document(
    company_id: str = Form(...),
    file: UploadFile = File(...)
):
    print("UPLOAD START")

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

    print(f"FILE READ: {len(file_content)} bytes")

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must be less than 10 MB"
        )

    file_path = UPLOAD_DIR / file.filename

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        print("FILE SAVED")

        documents = load_document(
            str(file_path)
        )

        print(f"PDF LOADED: {len(documents)} pages")

        chunks = split_documents(
            documents
        )

        print(f"CHUNKS CREATED: {len(chunks)}")

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the PDF"
            )

        print("GETTING VECTOR STORE...")

        vector_store = get_vector_store()

        print("STARTING INDEXING...")

        add_documents(
            vector_store,
            chunks,
            company_id
        )

        print("INDEXING COMPLETE")

    except HTTPException:
        if file_path.exists():
            file_path.unlink()
        raise

    except Exception:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(
            status_code=500,
            detail="DOCUMENT PROCESSING FAILED"
        )

    print("UPLOAD COMPLETE")

    return {
        "message": "Document uploaded and indexed successfully",
        "filename": file.filename,
        "company_id": company_id,
        "chunks": len(chunks)
    }

