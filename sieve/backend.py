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
        Build a fresh file backend in-memory. Be sure to call `FileBackend.dump` to persist.

        Args:
            filepath (str)
            query_string (str)
            initial_date (datetime)
        """
        return FileBackend(
            filepath=filepath,
            collection=Collection(query_string=query_string, date_updated=initial_date),
        )

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

    # pylint: disable-next=redefined-builtin
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
                return paper
        raise ValueError

    def papers(self) -> Iterable[Paper]:
        """
        Iterate over all papers.
        """
        yield from self.collection.papers

    def tag(self, stub: str) -> Tag:
        """
        Find and return a tag with the given stub.
        """
        for tag in self.tags():
            if tag.stub == stub:
                return tag
        raise ValueError

    def tags(self) -> Iterable[Tag]:
        """
        Iterate over all tags.
        """
        yield from self.collection.tags

    def add_tag(self, stub: str, items: list[str] | None = None) -> None:
        """
        Add a new tag to the collection.
        """
        tag = Tag.from_stub(stub)
        if items:
            tag.items.extend(items)
        self.collection.tags.append(tag)

    def update(self) -> None:
        """
        Extend the collection with any papers published since the last update.
        """
        new_papers = query(
            self.collection.query_string, until=self.collection.date_updated
        )
        self.collection.papers.extend(new_papers)
        self.collection.date_updated = datetime.now()
