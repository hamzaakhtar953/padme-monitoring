from datetime import datetime
from pydantic import BaseModel


class TrainMetadataModel(BaseModel):
    identifier: str
    title: str
    creator: str
    description: str
    version: str = "1.0"
    created_at: datetime = datetime.now()
