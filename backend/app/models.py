import uuid

from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field

from app.utils import MetricType

version_regex = "^(0|[1-9]|10)\\.(0|[1-9]|10)\\.(0|[1-9]|10)$"


class TrainMetadataBase(BaseModel):
    # TODO: use uuid.UUID instead
    identifier: str = Field(min_length=5, max_length=50)
    creator: str = Field(min_length=3, max_length=50)
    title: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=10, max_length=200)
    version: str = Field(pattern=version_regex, default="1.0.0")
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()


class TrainMetadataUpdate(BaseModel):
    creator: str | None = Field(min_length=3, max_length=50, default=None)
    title: str | None = Field(min_length=5, max_length=50, default=None)
    description: str | None = Field(min_length=10, max_length=200, default=None)
    version: str | None = Field(pattern=version_regex, default=None)
    updatedAt: datetime = datetime.now()


class JobMetadataBase(BaseModel):
    # TODO: use uuid.UUID instead
    identifier: str = Field(min_length=5, max_length=50)
    train_id: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=10, max_length=200)
    creator: str = Field(min_length=3, max_length=50)
    plannedRoute: list[Annotated[str, Field(min_length=3, max_length=50)]] = Field(
        min_length=1
    )
    currentStation: str
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()


class JobMetricMetadataCreate(BaseModel):
    metric_type: MetricType = Field(default=MetricType.cpu)
    job_id: str = Field(min_length=3, max_length=50)
    station_id: str = Field(min_length=3, max_length=50)
    value: str = Field(min_length=1, max_length=50)
    timestamp: datetime = datetime.now()


class JobMetricMetadataDelete(BaseModel):
    metric_id: uuid.UUID
    metric_type: MetricType
