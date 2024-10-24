"""
Simple API server.
"""

# pylint: disable=redefined-builtin

from enum import Enum
from datetime import datetime
from typing import Protocol, Self, Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sieve.config import SETTINGS
from sieve.backend import FileBackend
from sieve.models import Paper

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


backend = FileBackend.load(SETTINGS.file_backend)


class SortType(str, Enum):
    """
    Determines how the returned papers should be sorted.
    """

    DATE = "date"
    INTEREST = "interest"


class SortDirection(str, Enum):
    """
    Determines how the sorted papers should be organized.
    """

    ASCENDING = "ascending"
    DESCENDING = "descending"


class Sortable(Protocol):
    """
    Utility class capturing objects that can be ordered.
    """

    def __lt__(self, other: Self) -> bool: ...


class FilterType(str, Enum):
    """
    Determines which papers should be returned.
    """

    TODAY = "today"
    INTEREST = "interest"


class PapersMessage(BaseModel):
    """
    Parameterizes requests for papers.
    """

    sort_type: SortType = SortType.DATE
    sort_direction: SortDirection = SortDirection.DESCENDING
    filters: list[FilterType] = []

    def filter(self, paper: Paper) -> bool:
        """
        Check if the message accepts the paper based on the filters present.
        """
        if FilterType.TODAY in self.filters:
            today = datetime.today()
            if today.date() != paper.date_published.date():
                return False

        if FilterType.INTEREST in self.filters:
            if not paper.interest:
                return False

        return True

    @property
    def sort_key(self) -> Callable[[Paper], Sortable]:
        """
        Callable that can be passed as the `key` parameter to `sorted()` to implement the messages
        sort strategy.
        """
        match self.sort_type:
            case SortType.DATE:
                return lambda paper: paper.date_published

            # TODO: Use predicted likelihood of interest instead.
            case SortType.INTEREST:
                return lambda paper: 1 if paper.interest else 0


@app.get("/papers")
async def get_papers(message: PapersMessage = PapersMessage()):
    """
    Get all papers.
    """
    relevant_papers = [paper for paper in backend.papers() if message.filter(paper)]
    sorted_papers = sorted(
        relevant_papers,
        key=message.sort_key,
        reverse=(message.sort_direction == SortDirection.DESCENDING),
    )
    return [paper.id for paper in sorted_papers]


@app.get("/paper/{id}")
async def get_paper(id: str):
    """
    Get a paper by its identifier.
    """
    return backend.paper(id)


class SetInterestMessage(BaseModel):
    """
    Set the interest of a particular paper.
    """

    id: str
    interest: bool


@app.post("/interest")
async def set_paper_interest(message: SetInterestMessage):
    """
    Set the interest of a paper by identifier.
    """
    backend.paper(message.id).interest = message.interest
    backend.dump()
