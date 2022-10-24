import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
from MODULE import EMBED


class Member(Cog_Extention):

    @commands.Cog.listener()
    async def on_member_join(self, member):
      if member.guild.id == 912297466622251008:
        channel = member.guild.system_channel
        embed = EMBED.Embed()
        embed.add(name = "Welcome", value = f"{member.name} has droped in. \n \n 請到<#912301188530192404>閱讀版規後領取身分組。謝謝", inline = False)
        embed = embed.output()
        await channel.send(embed = embed)
      elif member.guild.id == 863269145981222942 :
        channel = self.client.get_channel(863276161236992011)
        await channel.send('欸幹竹子有人進來欸')


    @commands.Cog.listener()
    async def on_member_remove(self, member):
      if member.guild.id == 912297466622251008:
        channel = member.guild.system_channel
        embed = EMBED.Embed()
        embed.add(name = "Oh No!", value = f"{member.name} has gone.", inline = False)
        embed = embed.output()
        await channel.send(embed = embed)
      elif member.guild.id == 863269145981222942 :
        channel = self.client.get_channel(863276161236992011)
        await channel.send('幹又有人離開了啦！ 竹子管一下啦')


def setup(client):
    client.add_cog(Member(client))
