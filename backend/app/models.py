from datetime import datetime
from pydantic import BaseModel, Field

version_regex = "^(0|[1-9]|10)\\.(0|[1-9]|10)\\.(0|[1-9]|10)$"


class TrainMetadataBase(BaseModel):
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
