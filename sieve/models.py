"""
Model definitions for sieve's core objects.
"""

from __future__ import annotations

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
    interest: bool = False
    embedding: list[float] | None

    @property
    def rich_authors(self) -> str:
        """
        Authors of the paper rendered as a `rich`-compatible string.
        """
        match self.authors:
            case []:
                return ""
            case [author]:
                return author.split(" ")[-1]
            case [first, second]:
                first = first.split(" ")[-1]
                second = second.split(" ")[-1]
                return f"{first} and {second}"
            case [first, second, *rest]:
                first = first.split(" ")[-1]
                second = second.split(" ")[-1]
                return (
                    f"{first}, {second}, [dim]and[/dim] {len(rest)} [dim]others[/dim]"
                )


class Tag(BaseModel):
    """
    Tags are clusters of papers.
    """

    atoms: list[str]
    items: list[str]
    embedding: list[float] | None

    @property
    def stub(self) -> str:
        """
        Flattens the hierarchical tags to a single string.
        """
        return self.atoms.join("\\")

    @staticmethod
    def from_stub(stub: str) -> Tag:
        """
        Build a fresh tag from a given stub.
        """
        atoms = stub.split("\\")
        return Tag(atoms=atoms, items=[])
