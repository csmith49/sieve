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


@app.get("/papers")
async def get_papers():
    """
    Get all papers.
    """
    return [paper.id for paper in backend.papers()]


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
