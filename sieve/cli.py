"""
Simple CLI wrapper around `backend.FileBackend` instances.
"""

# pylint: disable=redefined-outer-name
# pylint: disable=redefined-builtin
# pylint: disable=function-redefined

from os import path, mkdir, remove as rm
from datetime import datetime
from functools import update_wrapper
from typing import Iterable

from rich import print as pprint
from rich.status import Status
from rich.table import Table
import click

from .backend import FileBackend
from . import arxiv


def pass_backend(f):
    """
    Passes the backend identified by the `Context.obj` value as the first argument to the command.
    """

    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        # The stored object is the backend filepath.
        if not path.exists(ctx.obj):
            print("No backend file. Run the init command.")
            raise click.Abort()
        backend = FileBackend.load(ctx.obj)
        return ctx.invoke(f, backend, *args, **kwargs)

    return update_wrapper(new_func, f)


@click.group()
@click.option("--backend-file", envvar="SIEVE_BACKEND_FILE", default="sieve")
@click.pass_context
def cli(ctx: click.Context, backend_file: str):
    """
    Query, store, and analyze arXiv papers.
    """
    backend_filepath = path.join(
        click.get_app_dir("Sieve", force_posix=True), backend_file
    )
    ctx.obj = backend_filepath


@cli.command()
@click.argument("query_string", type=str)
@click.option("--max_results", type=int, default=10)
def query(query_string: str, max_results: int):
    """
    Query the arXiv API and display the results.
    """
    results = arxiv.query(query_string, max_results=max_results)
    for paper in results:
        pprint(paper)


@cli.command()
@click.option("--query-string", type=str, default="cat:cs.AI")
@click.option("--initial-date", type=click.DateTime(), default=str(datetime.today()))
@click.pass_obj
def init(backend_filepath: str, query_string: str, initial_date: datetime):
    """
    Initialize a backend file.
    """
    # Ensure the app directory exists.
    app_directory = click.get_app_dir("Sieve", force_posix=True)
    if not path.exists(app_directory):
        mkdir(app_directory)

    if path.exists(backend_filepath):
        print("Cannot initialize backend -- already exists.")
        exit(-1)

    backend = FileBackend.initialize(
        filepath=backend_filepath, query_string=query_string, initial_date=initial_date
    )
    backend.dump()


@cli.command()
@click.pass_obj
def delete(backend_filepath: str):
    """
    Delete a backend file.
    """
    click.confirm("Are you sure? This cannot be undone.")
    if path.exists(backend_filepath):
        rm(backend_filepath)


@cli.command()
@pass_backend
def update(backend: FileBackend):
    """
    Read new entries from the arXiv API.
    """
    with Status("Fetching from arXiv..."):
        backend.update()
    backend.dump()


@cli.command()
@pass_backend
def details(backend: FileBackend):
    """
    See details about the backend file.
    """
    result = {
        "filepath": backend.filepath,
        "papers": len(backend.collection.papers),
        "tags": len(backend.collection.tags),
        "filesize": f"{path.getsize(backend.filepath)/(1<<20):.2f} MB",
    }
    pprint(result)


@cli.group()
def papers():
    """
    List and tag papers.
    """


@papers.command()
@click.option("--today", is_flag=True)
@pass_backend
def list(backend: FileBackend, today: bool):
    """
    List all papers.
    """
    todays_date = datetime.today().date()
    if today and backend.collection.date_updated.date() < todays_date:
        pprint("WARNING: cannot get papers today, not yet updated.")

    table = Table()
    table.add_column("id", style="green")
    table.add_column("title")
    table.add_column("authors")
    table.add_column("published", style="blue", justify="right")

    for paper in backend.papers():
        if today and paper.date_updated.date() < todays_date:
            continue

        table.add_row(
            paper.id, paper.title, paper.rich_authors, str(paper.date_updated.date())
        )

    pprint(table)


@papers.command()
@click.argument("id", type=str)
@click.argument("tags", type=str, nargs=-1)
@pass_backend
def tag(backend: FileBackend, id: str, tags: Iterable[str]):
    """
    Add tags to a paper.
    """
    for tag in backend.tags():
        if tag.stub in tags:
            tag.items.append(id)


@papers.command()
@click.argument("id", type=str)
@pass_backend
def details(backend: FileBackend, id: str):
    """
    List all stored details about the paper.
    """
    pprint(backend.paper(id))


@cli.group()
def tags():
    """
    Add, list, and update tags.
    """


@tags.command()
@pass_backend
def list(backend: FileBackend):
    """
    List all tags.
    """
    for tag in backend.tags:
        pprint(tag)


@tags.command()
@click.argument("tag", type=str)
@pass_backend
def add(backend: FileBackend, tag: str):
    """
    Add a fresh tag.
    """
    backend.add_tag(tag)
    backend.dump()


@tags.command()
@click.argument("tag", type=str)
@pass_backend
def papers(backend: FileBackend, tag: str):
    """
    All papers with the tag.
    """
    for id in backend.tag(tag).items:
        paper = backend.paper(id)
        pprint(paper)
