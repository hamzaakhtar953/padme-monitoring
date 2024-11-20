from fastapi import APIRouter

from app.api.routes import train

api_router = APIRouter()
api_router.include_router(train.router, prefix="/trains", tags=["trains"])
