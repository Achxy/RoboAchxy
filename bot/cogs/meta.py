from bot.utils import BaseCog
from discord.ext import commands
import discord


__cogs__ = ("Meta",)


class Meta(BaseCog):
    @commands.command()
    async def foo(self, ctx):
        await ctx.send("So far so good!")

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            title="Pong! 🏓",
            description=f"Current Latency of the bot is {round(self.bot.latency * 1000)}ms",
        )
        await ctx.reply(embed=embed)
