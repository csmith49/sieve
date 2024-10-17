"""
Simple API server.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "howdy y'all"}

@app.get("/paper/{paper_id}")
async def get_paper(paper_id: str):
    return {"paper_id": paper_id}