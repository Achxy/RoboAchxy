from discord import Message
from bot.utils import BaseCog
from discord.ext import commands
from bot.options import LOG_MAP
from re import search


class PatternLogger(BaseCog):
    @commands.Cog.listener("on_message")
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        if message.guild and (chnl := LOG_MAP.get(str(message.guild.id))) is not None:
            for items in chnl["triggers"]:
                if search(items["lex_regexp"], message.content, items["case_sensitive"] << 1) is not None:
                    channel = self.bot.get_channel(items["channel"])
                    await channel.send(f"{message.author} said \n\n\n{message.content}")  # type: ignore
