from contextlib import asynccontextmanager

from fastapi import FastAPI
from rdflib_sqlalchemy import registerplugins

from app.core.config import settings
from app.core.database import graph_singleton
from app.api.main import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Register SQLAlchemy plugins first time application is started
    registerplugins()
    yield
    # Add cleanup functions here before application shutdown
    graph_singleton.close_graph()


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)


@app.get("/healthy")
async def health_check():
    return {"status": "healthy"}


# Include all API routes
app.include_router(api_router)
