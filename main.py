
version = "0.0.0_development"
import requests

response = requests.get("https://api.github.com/repos/v2ray/v2ray-core/releases/latest")
print(response.json()["name"])



from os import name
from discord.activity import Game
from rich.progress import track
import pyfiglet,sys

from rich.console import Console
from rich import print
import logging
from rich.logging import RichHandler
from rich.style import Style
con = Console()
FORMAT = "%(message)s"
logging.basicConfig(
    level="WARN", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(console=con,markup=True)]
)
log = logging.getLogger("rich")


banner = pyfiglet.figlet_format("MegaBot")
banner = f"[purple]{banner}[/]"

error_console = Console(stderr=True, style="bold red")

import discord
from discord.ext import commands

client = commands.Bot(command_prefix=".")

cogs = []

import json

config = open('./config.json')
config = json.load(config)
log.debug( f"Config: {config}" )

print(banner)

for cog in track(config['cogs'],description="Loading Cogs"):
    if config['cogs'][cog]:
        cogs.append(f"cogs.{cog}")
    else:
        continue
    total = 0
    for cog in cogs:
        try:
            client.load_extension(cog)
            print(f"sucessfully loaded {cog}")
            total += 1
        except Exception as error:
            log.warning(f"Failed to load {cog}")
    print(f"all cogs loaded! ({total})")


@client.event
async def on_ready():
    con.clear()
    print(banner)
    con.rule("")
    print(f"\n[purple]{client.user}[/] [red]Ready![/]\nWith [green]{round(client.latency * 1000)}ms[/] of [red]ping[/]\nIm in [green]{len(client.guilds)}[/] [purple]servers[/]")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers"))
    len(client.guilds)

@client.command()
async def cogs(ctx):
    embed=discord.Embed(title="Cog", description="status", color=discord.Color.random())
    for cog in config['cogs']:
        if config['cogs'][cog] == True:
            value = "✅"
        else:
            value = "❌"
        embed.add_field(name=f"{cog}", value=value)
    await ctx.send(embed=embed)

@client.command(aliases=['ver', 'v', 'V'])
async def version(ctx):
    ver_msg = discord.Embed(
        title=f'Version: {version}',
        desc=f'I assume that you there, are a programmer or a or just a cheeky nerd who is interested in me (type "{config["prefix"]}abt" to know more about me and even access my github page)',
        footer="made by Dis-Code#0288",
        colour=discord.Colour.random()
    )
    await ctx.send(ver_msg)


try:
    client.run(config["token"])
except:
    log.critical(f"[red]{config['token']}[/red] is [white on red blink]NOT[/white on red blink] a valid token")
    input("")
    exit(1)