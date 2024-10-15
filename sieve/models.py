"""
Model definitions for sieve's core objects.
"""

from datetime import datetime
from pydantic import BaseModel


class Paper(BaseModel):
    """
    Papers are published units from the arXiv API.
    """

    id: str
    title: str
    authors: list[str]
    abstract: str
    date_published: datetime
    date_updated: datetime
    categories: list[str]
    embedding: list[float] | None


class Tag(BaseModel):
    """
    Tags are clusters of papers.
    """

    atoms: list[str]
    items: list[str]
    embedding: list[float] | None
