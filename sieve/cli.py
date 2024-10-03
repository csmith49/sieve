from rich import print as pprint
import click

from .arxiv import query

@click.command()
def run():
    for paper in query(max_results=10):
        pprint(paper)
