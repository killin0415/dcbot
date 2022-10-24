import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
from MODULE import EMBED


class GuildDC(Cog_Extention):

    @commands.Cog.listener()
    async def on_member_join(self, member):
      if member.guild.id == 973544147694813214:
        channel = member.guild.system_channel
        embed = EMBED.Embed()
        embed.add(name = "Welcome", value = f"{member.name} has droped in. \n \n 請到<#973935265456480269>領取身分組。謝謝", inline = False)
        embed = embed.output()
        await channel.send(embed = embed)
      


    @commands.Cog.listener()
    async def on_member_remove(self, member):
      if member.guild.id == 973544147694813214:
        channel = member.guild.system_channel
        embed = EMBED.Embed()
        embed.add(name = "Oh No!", value = f"{member.name} has gone.", inline = False)
        embed = embed.output()
        await channel.send(embed = embed)
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        role_dict = {
            '1️⃣': 973931641821081610,
            '2️⃣': 973931693922742333,
            '3️⃣': 973931762679939092
        }
        if payload.message_id == 974305239526146058:
            if str(payload.emoji) in role_dict:
                guild = self.client.get_guild(payload.guild_id)
                role = guild.get_role(role_dict[str(payload.emoji)])
                await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        role_dict = {
            '1️⃣': 973931641821081610,
            '2️⃣': 973931693922742333,
            '3️⃣': 973931762679939092
        }
        if payload.message_id == 974305239526146058:
            if str(payload.emoji) in role_dict:
                guild = self.client.get_guild(payload.guild_id)
                user = guild.get_member(payload.user_id)
                role = guild.get_role(role_dict[str(payload.emoji)])
                await user.remove_roles(role)
      


def setup(client):
    client.add_cog(GuildDC(client))
