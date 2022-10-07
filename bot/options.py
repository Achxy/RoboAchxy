from __future__ import annotations
from pathlib import Path
from json import loads
from os import environ

try:
    import dotenv

    dotenv.load_dotenv()
except ImportError:
    pass

BOT_DIR = Path(__file__).parent
ROOT_DIR = BOT_DIR.parent
COGS_DIR = BOT_DIR / "cogs"

with (ROOT_DIR / "config.json").open("r") as cfg:
    CONFIG = loads(cfg.read())


DISCORD_TOKEN: str = environ["DISCORD_TOKEN"]
POSTGRES_DSN: str = environ["POSTGRES_DSN"]
LOG_MAP: dict[str, dict[str, list[dict]]] = CONFIG["log_map"]
MAX_GUILD_PREFIX_LIMIT = 10
