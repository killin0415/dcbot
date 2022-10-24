import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
from MODULE.useful_function import func
from MODULE import EMBED
import datetime


class Help(Cog_Extention):
    @commands.group()
    async def help(self, ctx):
      if ctx.invoked_subcommand is None:
          embed = EMBED.Embed()
          embed.add(name='message', value='the commands about message(maybe)', inline=False)
          embed.add(name='manage', value='the commands about manage(maybe)', inline=False)
          embed.add(name='system', value='the commands about system(maybe)', inline=False)
          embed.add(name='english', value='the commands about english(maybe)', inline=False)
          embed.add(name='others', value='others commands', inline=False)
          embed = embed.output()
          embed.set_footer(text = "You can also type --help <name> for extra help message.")
          await ctx.send(embed=embed)

    @help.command()
    async def message(self, ctx):
      embed = EMBED.Embed()
      embed.add(name = '--say',value = "To let bot say something which behind the command",inline = False)
      embed.add(name = "--purge", value = "delete some message~~", inline = False)
      embed = embed.output()
      await ctx.send(embed=embed)

    @help.command()
    async def manage(self, ctx):
      embed = EMBED.Embed()
      embed.add(name = "--load", value = "To load the cog", inline = True)
      embed.add(name = "--reload", value = "To re-load the cog", inline = True)
      embed.add(name = "--unload", value = "To un-load the cog", inline = True)
      embed = embed.output()
      await ctx.send(embed=embed)

    @help.command()
    async def system(self, ctx):
      embed = EMBED.Embed()
      embed.add(name='--now', value='To get the current time', inline=False)
      embed.add(name='--ping', value='To get the ping delay', inline=False)
      embed = embed.output()
      await ctx.send(embed=embed)
    
    @help.command()
    async def english(self, ctx):
      embed = EMBED.Embed()
      embed.add(name='--search', value='To search the translation from english to chinese ', inline=False)
      embed.add(name = "--add", value = "To add a word and it's translation into the dictionary", inline = False)
      embed = embed.output()
      await ctx.send(embed=embed)
    
    @help.command()
    async def others(self, ctx):
      embed = EMBED.Embed()
      embed.add(name='--rank', value="To check your rank in this system \n It's broke now XD", inline=False) 
      embed = embed.output()
      await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
