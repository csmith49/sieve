"""
Simple CLI wrapper around `backend.FileBackend` instances.
"""

from os import path
from datetime import datetime

from rich import print as pprint
import click

from .backend import FileBackend
from . import arxiv

@click.group()
def without_backend():
    """
    Utilities for direct API access and backend creation.
    """

@without_backend.command()
@click.argument("query_string", type=str)
@click.option("--max_results", type=int, default=10)
def query(query_string: str, max_results: int):
    """
    Query the arXiv API and display the results.
    """
    results = arxiv.query(query_string, max_results=max_results)
    for paper in results:
        pprint(paper)


@without_backend.command()
@click.option("--backend-file", envvar="SIEVE_BACKEND_FILE", default=".sieve")
@click.option("--query-string", type=str, default="cat:cs.AI")
@click.option("--initial-date", type=click.DateTime(), default=str(datetime.today()))
def init(backend_file: str, query_string: str, initial_date: datetime):
    """
    Initialize a backend file.
    """
    backend_filepath = path.join(
        click.get_app_dir("Sieve", force_posix=True), backend_file
    )
    if path.exists(backend_filepath):
        print(f"Cannot initialize {backend_file} -- already exists.")
        exit(-1)

    backend = FileBackend.initialize(
        filepath=backend_filepath, query_string=query_string, initial_date=initial_date
    )
    backend.dump()


@click.group()
@click.option("--backend-file", envvar="SIEVE_BACKEND_FILE", default=".sieve")
@click.pass_context
def with_backend(ctx: click.Context, backend_file: str):
    """
    Utilities for manipulating sieve backend files.
    """
    backend_filepath = path.join(
        click.get_app_dir("Sieve", force_posix=True), backend_file
    )
    if not path.exists(backend_filepath):
        print(f"No {backend_file}. Run the init command first.")
        exit(-1)

    ctx.obj = FileBackend.load(backend_filepath)


@with_backend.command()
@click.pass_obj
def update(backend: FileBackend):
    """
    Read new entries from the arXiv API.
    """
    backend.update()
    backend.dump()


cli = click.CommandCollection(sources=[without_backend, with_backend])
"""
Entrypoint `click.Command` for the sieve CLI.
"""
