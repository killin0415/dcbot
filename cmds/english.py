import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
import json
from MODULE import EMBED 

with open('JSONHOME/english_dict.json', 'r', encoding='utf-8') as f:
    English_Dictionary = json.load(f)
    f.close()

def check(ctx):
    return ctx.author.id == 625302301313073192
  

class English(Cog_Extention):
  @commands.command()
  async def search(self, ctx: str, word):
    if word in English_Dictionary.keys():
        await ctx.send(f"I got the word\n{word} means '{English_Dictionary[word]}'")

    else:
        await ctx.send("I'm sorry,potato didn't know this word")

  @commands.command()
  async def add(self, ctx, en:str, ch:str):
    if en not in English_Dictionary.keys():
      English_Dictionary[en] = ch
      await ctx.send("新增成功")

      with open('JSONHOME/english_dict.json', 'w', encoding='utf8') as dataFile:
        json.dump(English_Dictionary, dataFile, ensure_ascii=False, indent=4)
    else:
      await ctx.send("there's already a word in the dictionary, please use --search to find the word.")

      
  @commands.check(check)
  @commands.command()
  async def delete(self, ctx, en: str):
    try:
      del English_Dictionary[en]
      with open('JSONHOME/english_dict.json', 'w', encoding='utf8') as dataFile:
          json.dump(English_Dictionary, dataFile, ensure_ascii=False, indent=4)
      embed = EMBED.Embed()
      embed.add(name = "--delete", value = f"delete {en} successfully",inline = False)
      embed = embed.output()
          
      await ctx.send(embed = embed)
    except KeyError:
      embed = EMBED.Embed()
      embed.add(name = "--delete", value = f"failed to delete {en} ",inline = False)
      embed = embed.output()      
      await ctx.send(embed = embed)

  @commands.check(check)
  @commands.command()
  async def change(self, ctx, en : str, ch : str):
    try:
      English_Dictionary[en] = ch
      with open('JSONHOME/english_dict.json', 'w', encoding='utf8') as dataFile:
          json.dump(English_Dictionary, dataFile, ensure_ascii=False, indent=4)
      embed = EMBED.Embed()
      embed.add(name = "--change", value = f"change {en} meaning into {ch} successfully",inline = False)
      embed = embed.output()     
      await ctx.send(embed = embed)
    except KeyError:
      embed = EMBED.Embed()
      embed.add(name = "--delete", value = f"failed to change {en} meaning",inline = False)
      embed = embed.output()      
      await ctx.send(embed = embed)



def setup(client):
    client.add_cog(English(client))
