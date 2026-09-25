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




import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from backend.app.services.ingestion import load_document
from backend.app.services.chunking import split_documents
from backend.app.services.embedding import create_embeddings

from backend.app.services.vector_store import (
    load_vector_store,
    add_documents,
    get_document_metadata,
    delete_document,
    get_company_documents
)

from backend.app.services.storage import (
    upload_file,
    delete_file
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

        embeddings = create_embeddings()

        vector_store = load_vector_store(
            embeddings
        )

    return vector_store


@router.post("/documents")
async def upload_document(
    company_id: str = Form(...),
    file: UploadFile = File(...)
):

    # -----------------------------
    # 1. Validate company_id
    # -----------------------------

    company_id = company_id.strip()

    if not company_id:

        raise HTTPException(
            status_code=400,
            detail="Company ID cannot be empty"
        )


    # -----------------------------
    # 2. Validate filename
    # -----------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )


    # -----------------------------
    # 3. Validate file type
    # -----------------------------

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )


    # -----------------------------
    # 4. Read uploaded file
    # -----------------------------

    file_content = await file.read()


    # -----------------------------
    # 5. Validate file size
    # -----------------------------

    if len(file_content) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=413,
            detail="File size must be less than 10 MB"
        )


    # -----------------------------
    # 6. Generate document ID
    # -----------------------------

    document_id = str(
        uuid.uuid4()
    )


    # -----------------------------
    # 7. Temporary local file path
    # -----------------------------

    file_path = UPLOAD_DIR / file.filename


    try:

        # -----------------------------
        # 8. Save file temporarily
        # -----------------------------

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(
                file_content
            )


        # -----------------------------
        # 9. Create B2 object path
        # -----------------------------

        object_name = (
            f"{company_id}/"
            f"{document_id}/"
            f"{file.filename}"
        )


        # -----------------------------
        # 10. Upload original PDF to B2
        # -----------------------------

        upload_file(
            str(file_path),
            object_name
        )


        # -----------------------------
        # 11. Extract document text
        # -----------------------------

        documents = load_document(
            str(file_path)
        )


        # -----------------------------
        # 12. Create chunks
        # -----------------------------

        chunks = split_documents(
            documents
        )


        if not chunks:

            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the PDF"
            )


        # -----------------------------
        # 13. Add metadata
        # -----------------------------

        for chunk in chunks:

            chunk.metadata["company_id"] = (
                company_id
            )

            chunk.metadata["document_id"] = (
                document_id
            )

            chunk.metadata["filename"] = (
                file.filename
            )


        # -----------------------------
        # 14. Get vector store
        # -----------------------------

        vector_store = get_vector_store()


        # -----------------------------
        # 15. Add chunks to Chroma
        # -----------------------------

        add_documents(
            vector_store,
            chunks
        )


    except HTTPException:

        if file_path.exists():

            file_path.unlink()

        raise


    except Exception as e:

        print(
            "UPLOAD ERROR:",
            repr(e)
        )

        if file_path.exists():

            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="Document processing failed"
        )


    finally:

        # -----------------------------
        # 16. Delete temporary file
        # -----------------------------

        if file_path.exists():

            file_path.unlink()


    # -----------------------------
    # 17. Return response
    # -----------------------------

    return {
        "message": "Document uploaded and indexed successfully",
        "document_id": document_id,
        "filename": file.filename,
        "company_id": company_id,
        "chunks": len(chunks)
    }


@router.get("/documents/{company_id}")
def list_documents(company_id: str):

    # -----------------------------
    # 1. Validate company_id
    # -----------------------------

    company_id = company_id.strip()

    if not company_id:

        raise HTTPException(
            status_code=400,
            detail="Company ID cannot be empty"
        )


    try:

        # -----------------------------
        # 2. Get company records
        # -----------------------------

        result = get_company_documents(
            company_id
        )


        # -----------------------------
        # 3. Group chunks into documents
        # -----------------------------

        documents = {}

        for metadata in result.get(
            "metadatas",
            []
        ):

            document_id = metadata.get(
                "document_id"
            )

            filename = metadata.get(
                "filename"
            )


            if not document_id:

                continue


            if document_id not in documents:

                documents[document_id] = {
                    "document_id": document_id,
                    "filename": filename,
                    "company_id": company_id
                }


        # -----------------------------
        # 4. Return document list
        # -----------------------------

        return {
            "company_id": company_id,
            "documents": list(
                documents.values()
            ),
            "total_documents": len(
                documents
            )
        }


    except Exception as e:

        print(
            "LIST DOCUMENTS ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch documents"
        )


@router.delete(
    "/documents/{company_id}/{document_id}"
)
def remove_document(
    company_id: str,
    document_id: str
):

    # -----------------------------
    # 1. Validate company_id
    # -----------------------------

    company_id = company_id.strip()


    # -----------------------------
    # 2. Validate document_id
    # -----------------------------

    document_id = document_id.strip()


    if not company_id:

        raise HTTPException(
            status_code=400,
            detail="Company ID cannot be empty"
        )


    if not document_id:

        raise HTTPException(
            status_code=400,
            detail="Document ID cannot be empty"
        )


    try:

        # -----------------------------
        # 3. Get document metadata
        # -----------------------------

        metadata = get_document_metadata(
            document_id
        )


        if not metadata:

            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )


        # -----------------------------
        # 4. Verify company ownership
        # -----------------------------

        if metadata.get(
            "company_id"
        ) != company_id:

            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )


        # -----------------------------
        # 5. Get filename
        # -----------------------------

        filename = metadata.get(
            "filename"
        )


        if not filename:

            raise HTTPException(
                status_code=500,
                detail="Document filename is missing"
            )


        # -----------------------------
        # 6. Create B2 object path
        # -----------------------------

        object_name = (
            f"{company_id}/"
            f"{document_id}/"
            f"{filename}"
        )


        # -----------------------------
        # 7. Get vector store
        # -----------------------------

        vector_store = get_vector_store()


        # -----------------------------
        # 8. Delete Chroma chunks
        # -----------------------------

        delete_document(
            vector_store,
            document_id
        )


        # -----------------------------
        # 9. Delete PDF from B2
        # -----------------------------

        delete_file(
            object_name
        )


        # -----------------------------
        # 10. Return response
        # -----------------------------

        return {
            "message": "Document deleted successfully",
            "document_id": document_id,
            "filename": filename,
            "company_id": company_id
        }


    except HTTPException:

        raise


    except Exception as e:

        print(
            "DELETE ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Document deletion failed"
        )