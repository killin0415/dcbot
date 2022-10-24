import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
from MODULE import EMBED


class GameDC(Cog_Extention):

    @commands.Cog.listener()
    async def on_member_join(self, member):
      if member.guild.id == 969596724383449098:
        channel = member.guild.system_channel
        embed = EMBED.Embed()
        embed.add(name = "Welcome", value = f"{member.name} has droped in. \n \n 請到<#970684551401734245>閱讀版規後領取身分組。謝謝", inline = False)
        embed = embed.output()
        await channel.send(embed = embed)
      


    @commands.Cog.listener()
    async def on_member_remove(self, member):
      if member.guild.id == 969596724383449098:
        channel = member.guild.system_channel
        embed = EMBED.Embed()
        embed.add(name = "Oh No!", value = f"{member.name} has gone.", inline = False)
        embed = embed.output()
        await channel.send(embed = embed)
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 970690551898857504:
            if str(payload.emoji) == "<:neko_hi:970690702214303814>":
                guild = self.client.get_guild(payload.guild_id)
                role = guild.get_role(970684022256726036)
                await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 970690551898857504:
            if str(payload.emoji) == "<:neko_hi:970690702214303814>":
                guild = self.client.get_guild(payload.guild_id)
                user = guild.get_member(payload.user_id)
                role = guild.get_role(970684022256726036)
                await user.remove_roles(role)
      


def setup(client):
    client.add_cog(GameDC(client))
