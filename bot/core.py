from discord import Message
from discord.ext.commands import Bot
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionNotFound
from .options import BOT_DIR, LOG_MAP
from pathlib import Path
from re import search
from importlib.util import spec_from_file_location


class RoboAchxy(Bot):
    async def load_extension_from_path(self, path: Path, package: Path = BOT_DIR):
        stem = path.stem
        spec = spec_from_file_location(stem, str(path))
        name = self._resolve_name(stem, str(package))
        if name in self.extensions:
            raise ExtensionAlreadyLoaded(name)
        if spec is None:
            raise ExtensionNotFound(name)
        await self._load_from_module_spec(spec, name)

    async def on_message(self, message: Message):
        if message.author.bot:
            return
        if message.guild and (chnl := LOG_MAP.get(str(message.guild.id))) is not None:
            for items in chnl["triggers"]:
                if search(items["lex_regexp"], message.content, items["case_sensitive"] << 1) is not None:
                    channel = self.get_channel(items["channel"])
                    await channel.send(f"{message.author} said \n\n\n{message.content}")  # type: ignore
