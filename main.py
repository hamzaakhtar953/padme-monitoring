from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.log_config import logger
from database import rdf_graph
from routers import train


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    logger.warning("Shutting down application and closing database connections")
    rdf_graph.close_graph()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Welcome to PADME Monitoring"}


app.include_router(train.router)
