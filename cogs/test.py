import discord
from discord.ext import commands


# rich import
from rich.console import Console
from rich import print
import logging
from rich.logging import RichHandler
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")








class Ping(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(description="Used to check bot's ping")
    async def ping(self, ctx):
        try:
            embed=discord.Embed(title="Pong!", description=f"{round(self.client.latency * 1000)}ms", color=0xff0000)
            await ctx.send(embed=embed)
        except Exception as error:
            log.warning("There was an error trying to use this command (ping)")
def setup(client):
    client.add_cog(Ping(client))