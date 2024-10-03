from datetime import datetime
from pydantic import BaseModel

class Paper(BaseModel):
    id: str
    title: str
    authors: list[str]
    abstract: str
    date_published: datetime
    date_updated: datetime
    embedding: list[float] | None

class Tag(BaseModel):
    atoms: list[str]
    items: list[str]
