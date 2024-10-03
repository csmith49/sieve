"""
Utilities for interacting with the arXiv API. For more details see the user manual at:

https://info.arxiv.org/help/api/user-manual.html
"""

from typing import Iterable, Any
from time import sleep
from datetime import datetime
from urllib.request import urlopen
from feedparser import parse
from .models import Paper


def html_escaping(string: str) -> str:
    """
    Replaces certain characters in the input string with their escaped HTML equivalent.
    """
    replacements = [('"', "%22"), (" ", "+"), ("(", "%28"), (")", "%29")]

    for source, destination in replacements:
        string = string.replace(source, destination)

    return string


def search_url(query_string: str, page: int = 0, max_results: int = 1000) -> str:
    """
    Generate a URL with the provided parameters according to arXiv's API.

    Args:
        query_string (str): Query string, follows the arXiv API (with unescaped special characters).

        page (int, default=0): The page of results to grab.

        max_results (int, default=1000): Maximum number of entries per page.

    Returns:
        str: A URL encoding the provided parameters according to the API.
    """
    kwargs = {
        "search_query": html_escaping(query_string),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "start": page * max_results,
        "max_results": max_results,
    }
    kwarg_string = "&".join(f"{key}={value}" for key, value in kwargs.items())
    return f"http://export.arxiv.org/api/query?{kwarg_string}"


def paper_from_arxiv_entry(entry: dict[str, Any]) -> Paper:
    """
    Build a `Paper` from an entry in arXiv's Atom feed.
    """
    return Paper(
        id=entry["id"],
        title=" ".join(entry["title"].replace("\n", " ").split()),
        authors=[author["name"] for author in entry["authors"]],
        abstract=entry["summary"].replace("\n", " "),
        date_published=datetime(*entry["published_parsed"][:6]),
        date_updated=datetime(*entry["updated_parsed"][:6]),
        embedding=None,
    )


def get_feed(
    url: str, backoff_scaling: float = 1.5, max_tries: int = 10
) -> dict[str, Any]:
    """
    Get the feed at the given URl as a JSON-style dict.

    Args:
        url (str)

        backoff_scaling (float, default=1.5): How much to scale the wait time by whenever a new try is made.
    """

    for current_try in range(max_tries):
        try:
            return parse(urlopen(url).read().decode("utf-8"))
        except:
            sleep(3 * backoff_scaling**current_try)

    raise ValueError


def query(
    query_string: str, until: datetime | None = None, max_results: int | None = None
) -> Iterable[Paper]:
    # At least one stop condition needs to be set.
    if until is None and max_results is None:
        raise ValueError

    page, count = 0, 0

    while True:

        url = search_url(query_string, page=page, max_results=min(max_results, 1000))
        data = get_feed(url)

        for entry in data["entries"]:
            paper = paper_from_arxiv_entry(entry)
            yield paper_from_arxiv_entry(entry)

            # After we've yielded a `Paper`, check that we haven't exceeded our limit. If we have, it's time to stop.
            count += 1
            if max_results is not None and count >= max_results:
                return

            # If the paper was published _before_ the optional `until` argument, stop the iteration. We don't need it.
            if until and paper.date_published < until:
                return

        page += 1
