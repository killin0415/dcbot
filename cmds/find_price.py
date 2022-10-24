import nextcord
from nextcord import Embed
from nextcord.ext import commands, tasks, menus
from core.classes import Cog_Extention
from MODULE import EMBED
from MODULE.useful_function import To_string
from oauth2client import client
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import datetime

with open('JSONHOME/data.json', 'r', encoding='utf-8') as f:
    data_dict = json.load(f)
    f.close()


class MyEmbedFieldPageSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=2)

    async def format_page(self, menu, entries):
        embed = Embed(title="Entries")
        keys = entries.keys()
        for key in keys:
            embed.add_field(name=key, value=To_string(
                entries[key]), inline=True)
        embed.set_footer(
            text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
        return embed


class Dropdown(nextcord.ui.Select):
    def __init__(self, client, ctx):

        # Set the options that will be presented inside the dropdown
        data_keys = data_dict.keys()
        self.client = client
        options = []
        for data in data_keys:
            options.append(nextcord.SelectOption(
                label=data, description=f'{data}的選擇'))

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select one of these option...',
                         min_values=1, max_values=1, options=options)
        self.embed = EMBED.Embed()
        self.item_dict = {}
        self.i = 0
        self.item_keys = []
        self.ctx = ctx

    async def callback(self, interaction: nextcord.Interaction):

        self.item_dict = data_dict[self.values[0]]
        self.item_keys = list(self.item_dict.keys())

        pages = menus.ButtonMenuPages(
            source=MyEmbedFieldPageSource(self.item_dict),
            clear_buttons_after=True,
        )
        await pages.start(self.ctx)
        # await interaction.response.send_message(embed=embed, VIEW = self)


class DropdownView(nextcord.ui.View):
    def __init__(self, client, ctx):
        super().__init__()
        self.client = client
        self.ctx = ctx
        # Adds the dropdown to our view object.
        self.add_item(Dropdown(self.client, self.ctx))


class price(Cog_Extention):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # an attribute we can access from our task
        self.counter = 0
        # start the task to run in the background
        self.my_background_task.start()

    @tasks.loop(time=[datetime.time(hour=0)])
    async def my_background_task(self):
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'JSONHOME/python_API.json', scope)
        Client = gspread.authorize(creds)
        PythonSheet = Client.open("原X屋特價,內測中!!").sheet1

        i = 0
        list_ = []
        with open('JSONHOME/name.json', 'r', encoding='utf-8') as f:
            name_list = json.load(f)
            f.close()

        dict = {}
        sheet = PythonSheet.get_all_values()
        l = len(sheet)
        while i < l:
            item = sheet[i][1]
            if item in name_list:
                item_dict = dict[item] if item in dict.keys() else {}
                name = sheet[i][0]
                money = sheet[i][2]
                min_money = sheet[i][6]
                price_difference = sheet[i][7]
                time = sheet[i][5]
                item_dict[name] = [money, min_money, price_difference, time]
                dict[item] = item_dict
            i += 1
        with open('JSONHOME/data.json', 'w', encoding='utf8') as dataFile:
            json.dump(dict, dataFile, ensure_ascii=False, indent=4)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.client.wait_until_ready()  # wait until the bot logs in

    @commands.command()
    async def colour(self, ctx):
        """Sends a message with our dropdown containing colours"""

        # Create the view containing our dropdown
        view = DropdownView(self.client, ctx)

        # Sending a message containing our view
        await ctx.send('Pick an item:', view=view)


def setup(client):
    client.add_cog(price(client))


# print(PythonSheet.cell(100, 1).value)

# 將符合json項目的做成一個二維dict(item: (name: [money, min_money, price difference]))
# 將dict.keys()做成select menu透過command觸發
# 找到目前品項後存取品項所代表的dict->item_dict
# 將item_dict.keys()做成embed(or selct menu?)
# 對找到的品項將item_dict對應到的array做成embed輸出
