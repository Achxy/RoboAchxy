from ..utils import BaseCog
from discord.ext import commands


class Meta(BaseCog):
    @commands.command()
    async def foo(self, ctx):
        await ctx.send("So far so good!")


async def setup(bot):
    print("Omggg we are here in a cog", bot)
