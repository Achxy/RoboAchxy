from pathlib import Path
from json import loads
from os import getenv

BOT_DIR = Path(__file__).parent
ROOT_DIR = BOT_DIR.parent

with open(ROOT_DIR / "config.json") as cfg, open(ROOT_DIR / ".env") as env:
    CONFIG = loads(cfg.read())
    ENV = loads(env.read())


DISCORD_TOKEN: str = getenv("DISCORD_TOKEN") or ENV["DISCORD_TOKEN"]
LOG_MAP: dict[str, dict[str, list[dict]]] = CONFIG["log_map"]
