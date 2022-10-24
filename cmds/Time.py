import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
from MODULE.useful_function import func
import datetime

class Time(Cog_Extention):
    @commands.command()
    async def now(self, ctx):
        await ctx.send(func.get_date())


def setup(client):
    client.add_cog(Time(client))
