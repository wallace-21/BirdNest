from fastapi import APIRouter
from app.api.v1.endpoints import birds
from app.api.v1.endpoints import ai_agent
api_router = APIRouter()

api_router.include_router(birds.router, prefix="/birds", tags=["birds"])
api_router.include_router(ai_agent.router, prefix="/ai", tags=["AI Agent"])
