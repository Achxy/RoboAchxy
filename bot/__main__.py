from .core import RoboAchxy
from discord import Intents
from .options import DISCORD_TOKEN


def main():
    bot = RoboAchxy(command_prefix="avi", intents=Intents.all())
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
