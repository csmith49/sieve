"""
Config options!
"""

from os import path
from pydantic import BaseModel

CONFIG_PATH = "config.json"
"""
Default location for the configuration file.
"""

class Config(BaseModel):
    """
    Configuration!
    """

    openai_api_key: str | None = None
    file_backend: str | None = None

# If there is no provided config file, write the defaults to disc.
if not path.exists(CONFIG_PATH):
    default_settings = Config()
    with open(CONFIG_PATH, encoding="utf-8") as f:
        f.write(default_settings.model_dump_json())

with open(path.join("config.json"), encoding="utf-8") as f:
    SETTINGS = Config.model_validate_json(f.read())
