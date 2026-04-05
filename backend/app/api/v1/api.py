from fastapi import APIRouter
from app.api.v1.endpoints import documents, jobs, websocket

api_router = APIRouter()

api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
