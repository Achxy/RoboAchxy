from bot.utils import BaseCog
from discord.ext import commands


__cogs__ = ("Meta",)


class Meta(BaseCog):
    @commands.command()
    async def foo(self, ctx):
        await ctx.send("So far so good!")
