from discord import Client, Message
from .options import LOG_MAP


class RoboAchxy(Client):
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        if message.guild and (chnl := LOG_MAP.get(str(message.guild.id))) is not None:
            for items in chnl["triggers"]:
                cmp = items["lex"], message.content
                l, r = map(str.lower, cmp) if not items["case_sensitive"] else cmp
                if l in r:
                    channel = self.get_channel(items["channel"])
                    await channel.send(f"{message.author} said \n\n\n{message.content}")  # type: ignore


print(LOG_MAP)
