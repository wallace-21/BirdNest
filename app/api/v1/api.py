from fastapi import APIRouter
from app.api.v1.endpoints import birds

api_router = APIRouter()

api_router.include_router(birds.router, prefix="/birds", tags=["birds"])
