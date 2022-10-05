from __future__ import annotations
from pathlib import Path
from discord.ext import commands
from _typeshack import RoboAchxy
from options import BOT_DIR


class BaseCog(commands.Cog):
    def __init__(self, bot: RoboAchxy) -> None:
        self.bot = bot


def define_cogs(*cogs: type[BaseCog]):
    async def setup(bot: RoboAchxy):
        for cog in cogs:
            await bot.add_cog(cog(bot))

    return setup
