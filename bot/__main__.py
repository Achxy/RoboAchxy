from .core import RoboAchxy
from discord import Intents
from .options import DISCORD_TOKEN


bot = RoboAchxy(command_prefix=None, intents=Intents.all())
bot.run(DISCORD_TOKEN)
