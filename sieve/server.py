"""
Simple API server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sieve.config import SETTINGS
from sieve.backend import FileBackend

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
    return [paper.id for paper in backend.papers()]


@app.get("/paper/{id}")
async def get_paper(id: str):
    return backend.paper(id)


class InterestResponse(BaseModel):
    id: str
    interest: bool


@app.post("/interest")
async def set_paper_interest(response: InterestResponse | None = None):
    backend.paper(response.id).interest = response.interest
    backend.dump()
