from nextcord import Interaction, Permissions, SlashOption
import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
import asyncio

guild_id = 863269145981222942


def check(ctx: commands.Context):
    if ctx.guild.id != guild_id:
        return False
    for role in ctx.author.roles:
        if role.id == 863269353125969920:
            return True
    else:
        return False


class Mute(Cog_Extention):
    @nextcord.slash_command(name="mute", description="mute someone", guild_ids=[863269145981222942])
    async def mute(self, interaction: Interaction, mute_user: nextcord.Member = SlashOption(required=True), time=SlashOption(required=True, description='How many seconds')):
        for i in interaction.user.roles:
            if i.permissions.administrator:
                s = int(time[:-1])
                channel = interaction.channel
                role = interaction.guild.get_role(998550407586525266)
                await mute_user.add_roles(role)
                await interaction.response.send_message(f"{mute_user.mention} has been muted for {s}s.")
                await mute_user.send(f"You have been muted for {s}s, you can't talk or get into voice channel right now.If you got any problem or bug, please tell to the administrator.")
                await asyncio.sleep(s)
                await mute_user.remove_roles(role)
                await mute_user.send("Congradulation, now you're been unmuted")
                await channel.send(f"{mute_user.mention} has been unmuted.")
            break
        else:
            await interaction.response.send_message('You are not be allowed to use this command')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('hello')

    @nextcord.slash_command(name="hello", description="say hello to bot", guild_ids=[863269145981222942])
    async def hello(self, interaction: Interaction):
        author = str(interaction.user)
        await interaction.response.send_message(f"hello {author[:-5]} :)")


def setup(client):
    client.add_cog(Mute(client))
