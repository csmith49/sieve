"""
Utilities for embedding text strings.
"""

import dotenv
from openai import OpenAI

from sieve.config import SETTINGS

dotenv.load_dotenv(".env", override=True)
_CLIENT = OpenAI(api_key=SETTINGS.openai_api_key)


def embed(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """
    ...
    """
    response = _CLIENT.embeddings.create(input=text, model=model)
    return response.data[0].embedding
