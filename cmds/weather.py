import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
import urllib.parse
import urllib.request
import json
from MODULE.EMBED import Embed

 
def get_weather()->dict: 
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-067"

    headers = {"Authorization": "CWB-85C4471E-2957-46B0-A213-49DB4CA7D440"}

    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    hjson = json.loads(response.read())
    bdata = hjson['records']['locations'][0]['location']

    data = {}

    key_list = ['前金區', '岡山區', '前鎮區', '美濃區', '小港區', '鹽埕區', '林園區', '左營區', '三民區',
                '新興區', '鳥松區', '苓雅區', '橋頭區', '旗津區', '鳳山區', '鼓山區', '大寮區', '楠梓區', '旗山區']

    for i in bdata:
        key = i["locationName"]
        if key in key_list:
            value = i['weatherElement'][10]['time']
            data[key] = value
            for j in data[key]:
                j['elementValue'] = j['elementValue'][0]['value'].replace('。', "\n")
                j['startTime'] = j['startTime'][5:-3]
                j['endTime'] = j['endTime'][5:-3]

    return data
    
class Dropdown(nextcord.ui.Select):
    def __init__(self, data):

        # Set the options that will be presented inside the dropdown
        self.data = data
        options = []
        for choose in data:
            options.append(nextcord.SelectOption(
                label=choose, description=f'{choose}的天氣預報'))

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select one of these option...',
                         min_values=1,max_values=1, options=options)
    async def callback(self, interaction: nextcord.Interaction):
        self.choose: list = self.data[self.values[0]]
        embed = Embed()
        for i in range(2, len(self.choose), 2):
            embed.add(name = f"{self.choose[i]['startTime']}-{self.choose[i]['endTime']}",
                      value=self.choose[i]['elementValue'])
            embed.add(name = f"{self.choose[i+1]['startTime']}-{self.choose[i+1]['endTime']}",
                      value=self.choose[i+1]['elementValue'])
           
            
            

        await interaction.response.send_message(embed=embed.output())
    
class DropdownView(nextcord.ui.View):
    def __init__(self, data):
        super().__init__()
        self.data = data
        # Adds the dropdown to our view object.
        self.add_item(Dropdown(self.data))

 
class Weather(Cog_Extention):
    @commands.command()
    async def weather(self, ctx: commands.Context):
        view = DropdownView(get_weather())
        await ctx.send(view=view)

        
 
def setup(client):
    client.add_cog(Weather(client))