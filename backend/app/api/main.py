from fastapi import APIRouter

from app.api.routes import train, station, job

api_router = APIRouter()
api_router.include_router(train.router, prefix="/trains", tags=["trains"])
api_router.include_router(station.router, prefix="/stations", tags=["stations"])
api_router.include_router(job.router, prefix="/jobs", tags=["jobs"])
