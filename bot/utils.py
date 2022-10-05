from __future__ import annotations
from discord.ext import commands
from bot._typeshack import RoboAchxy


class BaseCog(commands.Cog):
    def __init__(self, bot: RoboAchxy) -> None:
        self.bot = bot
