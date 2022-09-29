from pathlib import Path
from json import loads
from os import getenv

BOT_DIR = Path(__file__).parent
ROOT_DIR = BOT_DIR.parent

with (ROOT_DIR / "config.json").open("r") as cfg:
    CONFIG = loads(cfg.read())
if (env_path := (ROOT_DIR / ".env")).exists():
    with env_path.open("r") as env:
        ENV = loads(env.read())
else:
    ENV = {}


DISCORD_TOKEN: str = getenv("DISCORD_TOKEN") or ENV["DISCORD_TOKEN"]
LOG_MAP: dict[str, dict[str, list[dict]]] = CONFIG["log_map"]
