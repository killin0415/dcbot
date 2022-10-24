import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
import json
import datetime

with open('JSONHOME/roles.json', 'r', encoding='utf-8') as f:
    roles = json.load(f)
    f.close()
    
def check(ctx):
    return ctx.author.id == 625302301313073192

class RoleDropdown(nextcord.ui.Select):
    def __init__(self, client, ctx):

        # Set the options that will be presented inside the dropdown
        self.client = client
        self.ctx = ctx
        self.l = len(roles.keys())
        options = []
        for data in roles.items():
            options.append(nextcord.SelectOption(
                label=data[0], description=f'{data[0]}', value=data[1]))

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select one of these roles...',
                         max_values=self.l, options=options)
    async def callback(self, interaction: nextcord.Interaction):
        for value in self.values:
            guild = self.client.get_guild(855054575899377725)
            user = self.ctx.author      
            role = guild.get_role(int(value))    
            await user.add_roles(role)  
        await interaction.response.send_message("success")
    
class RoleDropdownView(nextcord.ui.View):
    def __init__(self, client, ctx):
        super().__init__()
        self.client = client
        # Adds the dropdown to our view object.
        self.add_item(RoleDropdown(self.client, ctx))
        
class Roles(Cog_Extention):
    
    @commands.command()
    async def RoleCommands(self, ctx: commands.Context):
        view = RoleDropdownView(self.client, ctx)
        ctx.send(view=view)
        
def setup(client):
    client.add_cog(Roles(client))