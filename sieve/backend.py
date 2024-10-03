"""
The backend serves an interface for manipulating and storing papers and tags.
"""

from __future__ import annotations

from typing import Iterable
from datetime import datetime

from pydantic import BaseModel, Field
from .models import Paper, Tag
from .arxiv import query


class Collection(BaseModel):
    """
    Aggregation of papers and tags.
    """

    query_string: str
    date_updated: datetime = Field(default_factory=datetime.now)
    papers: list[Paper] = []
    tags: list[Tag] = []


class FileBackend:
    """
    Exposes papers and tags saved in a collection file.
    """

    @staticmethod
    def initialize(
        filepath: str, query_string: str, initial_date: datetime
    ) -> FileBackend:
        """
        Args:
            filepath (str)
            query_string (str)
            initial_date (datetime)
        """
        collection = Collection(query_string=query_string, date_updated=initial_date)
        backend = FileBackend(filepath=filepath, collection=collection)

        backend.dump()

        return backend

    @staticmethod
    def load(filepath: str) -> FileBackend:
        """
        Args:
            filepath (str)
        """
        with open(filepath, "r", encoding="utf-8") as f:
            collection = Collection.model_validate_json(f.read())

        return FileBackend(filepath=filepath, collection=collection)

    def __init__(self, filepath: str, collection: Collection) -> None:
        """
        Args:
            filepath (str): Filepath where the collection is stored.
        """
        self.filepath = filepath
        self.collection = collection

    def dump(self) -> None:
        """
        Writes the current contents of the collection to the collection file.
        """
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(self.collection.model_dump_json())

    def ids(self) -> Iterable[str]:
        """
        Iterate over identifiers of all papers.
        """
        for paper in self.papers():
            yield paper.id

    def paper(self, id: str) -> Paper:
        """
        Find and return a paper with the given id.

        Args:
            id (str): Identifier for the paper to be found.

        Raises:
            ValueError: if no such paper exists.
        """
        for paper in self.papers():
            if paper.id == id:
                return Paper
        raise ValueError

    def papers(self) -> Iterable[Paper]:
        """
        Iterate over all papers.
        """
        yield from self.collection.papers

    def tags(self) -> Iterable[Tag]:
        """
        Iterate over all tags.
        """
        yield from self.collection.tags

    def update(self) -> None:
        new_papers = query(
            self.collection.query_string, until=self.collection.date_updated
        )
        self.collection.papers.extend(new_papers)
