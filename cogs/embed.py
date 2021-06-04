import discord
from discord import client
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



class Embed(commands.Cog):
    def __init__(self,client):
        self.client = client
    @commands.command(pass_context=True,alieses=["hyperlink"])
    async def hl(self,ctx, linkName, heading, link):
        hyper_link = discord.Embed(
            title=linkName,
            description=f"***[{heading}]({link})***",
            color=discord.Colour.random()
        )
        hyper_link.set_footer(text=f"requested by {ctx.message.author}")
        await ctx.send(embed=hyper_link)
 
def setup(client):
    client.add_cog(Embed(client))