import nextcord
from nextcord.ext import commands
import os
from core.classes import Cog_Extention
from MODULE import EMBED
import requests

from nextcord.webhook import sync

intents = nextcord.Intents.all()
client = commands.Bot(command_prefix='--', intents=intents)
client.remove_command('help')
TOKEN = "OTA1NDA1ODM2OTg4Mzk1NTQw.GN-beG.74xkeytc39RS_9yc3tYnMEhdaf6XnH3FCbzEOI"


def check(ctx):
    return ctx.author.id == 625302301313073192

@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(name='--help helps', type=nextcord.ActivityType.listening))
    print('>> Bot is online ')
    r = requests.head(url="https://discord.com/api/v1")
    try:
        print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
    except:
        print("No rate limit")


@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)} (ms)')


@client.command()
@commands.check(check)
async def load(ctx, file_name):
    client.load_extension(f"cmds.{file_name}")
    embed = EMBED.Embed()
    embed.add("--load", f"{file_name} loaded successfully", False)
    embed = embed.output()
    await ctx.send(embed=embed)


@client.command()
@commands.check(check)
async def reload(ctx, file_name):
    client.reload_extension(f"cmds.{file_name}")
    embed = EMBED.Embed()
    embed.add('--reload', f"{file_name} re-loaded successfully", False)
    embed = embed.output()
    await ctx.send(embed=embed)


@client.command()
@commands.check(check)
async def unload(ctx, file_name):
    client.unload_extension(f"cmds.{file_name}")
    embed = EMBED.Embed()
    embed.add('--unload', f"{file_name} un-loaded successfully", False)
    embed = embed.output()
    await ctx.send(embed=embed)


for file in os.listdir('./cmds'):
    if file.endswith('.py'):
        client.load_extension(f"cmds.{file[:-3]}")

if __name__ == "__main__":
    client.run(TOKEN)
