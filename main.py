
version = "0.1.1_development"
import requests

response = requests.get("https://api.github.com/repos/mega145/Megabot/releases/latest",headers={"owner":"mega145","repo":"Megabot"})
try:
    if response.json()["name"] != version:
        out_of_date = True
        newest = response.json()["name"]
except Exception:
    out_of_date = True
    newest = None


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

try:
    config = open('./config_dev.json')
    config = json.load(config)
except Exception:
    pass
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
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements :rolling_eyes:.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the requirements :angry:")

@client.event
async def on_ready():
    con.clear()
    print(banner)
    con.rule("")
    print(f"\n[purple]{client.user}[/] [red]Ready![/]\nWith [green]{round(client.latency * 1000)}ms[/] of [red]ping[/]\nIm in [green]{len(client.guilds)}[/] [purple]servers[/]")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers"))
    if out_of_date:
        log.warning(f"The version you are using is [red]Out of date[/]\nthe [blue on red]newest[/] version is [green]{newest}[/]")
    AwakenChannel = client.get_channel(config["info_channel"])
    await AwakenChannel.send("Bot is now online")

@client.command(aliases=["c","cog"])
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

# scrapped idea 
'''
@client.command()
async def reload(ctx):
    
    for cog in cogs:
        client.unload_extension(cog)
    
    for cog in track(config['cogs'],description="Reloading Cogs"):
        if config['cogs'][cog]:
            cogs.append(f"cogs.{cog}")
        else:
            continue
    total = 0
    for cog in cogs:
        try:
            client.load_extension(cog)
            # print(f"sucessfully loaded {cog}")
            total += 1
        except Exception as error:
            log.warning(f"Failed to load {cog}")
    print(f"all cogs loaded! ({total})")
'''

try:
    client.run(config["token"])
except:
    log.critical(f"[red]{config['token']}[/red] is [white on red blink]NOT[/white on red blink] a valid token")
    input("")
    exit(1)
