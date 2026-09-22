from fastapi import FastAPI

from backend.app.api.chat import router as chat_router
from backend.app.api.documents import router as documents_router


app = FastAPI(
    title="AI Customer Support Assistant"
)


app.include_router(chat_router)
app.include_router(documents_router)