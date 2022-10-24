import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
from MODULE import EMBED
import json

with open('JSONHOME/reaction_role.json', 'r', encoding='utf-8') as f:
    reaction_role = json.load(f)


class Role(Cog_Extention):

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 912316581571350578 or payload.message_id == 912502713814769684:
            if str(payload.emoji) == "<:neko_hi:912313924383281163>":
                guild = self.client.get_guild(payload.guild_id)
                role = guild.get_role(912301547487129601)
                await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 912316581571350578:
            if str(payload.emoji) == "<:neko_hi:912313924383281163>":
                guild = self.client.get_guild(payload.guild_id)
                user = guild.get_member(payload.user_id)
                role = guild.get_role(912301547487129601)
                await user.remove_roles(role)


def setup(client):
    client.add_cog(Role(client))
