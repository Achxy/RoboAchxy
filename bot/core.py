from discord.ext import commands
from bot.cogs import entry as extension_entry_point


class RoboAchxy(commands.Bot):
    async def setup_hook(self) -> None:
        await extension_entry_point(self)
