from collections.abc import Iterator
from pathlib import Path
from types import ModuleType
from bot.options import COGS_DIR
from bot._typeshack import RoboAchxy
from bot.utils import BaseCog
from importlib.machinery import SourceFileLoader
from asyncio import gather


GLOB_PATTERN = "*.py"
PROHIBITED_STEMS = ("__init__", "__main__")
COGS_ATTRIBUTE = "__cogs__"


def _resolve(path: Path) -> ModuleType:
    return SourceFileLoader(path.stem, str(path)).load_module()


def get_cogs() -> Iterator[type[BaseCog]]:
    for file in COGS_DIR.glob(GLOB_PATTERN):
        if file.stem in PROHIBITED_STEMS:
            continue
        space = _resolve(file)
        for cog in getattr(space, COGS_ATTRIBUTE, []):
            yield getattr(space, cog)


async def entry(bot: RoboAchxy) -> None:
    cogs = (bot.add_cog(cog(bot)) for cog in get_cogs())
    await gather(*cogs)
