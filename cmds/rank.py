import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
from MODULE import level as levels
from MODULE import EMBED
import json


def dict_to_class(id, dict):
    id = str(id)
    item = dict[id]
    name = item['name']
    level = item['level']
    exp = item['exp']
    ranklimit = item['ranklimit']
    rank = item['rank']
    fb = item['fb']

    player = levels.Player(id, name, level=level, exp=exp,
                           ranklimit=ranklimit, rank=rank, fb=fb)
    return player


def update_rank(player, level_rank):
    record = -1
    exp = player.exp/(10**len(str(player.ranklimit)))
    level = player.level+exp
    key = str(player.id)
    for i in range(len(level_rank)):
        if level_rank[i][0] == key:
            level_rank[i][1] = level
            record = i
        break
    if record == -1:
        level_rank.append([key, level])
        level_rank = sorted(level_rank, key=lambda x: x[1], reverse=True)
        player.rank = level_rank.index([key, level]) + 1
    else:
        if record>0:
          while level_rank[record][1] > level_rank[record-1][1]:
              level_rank[record][1], level_rank[record -
                                                1][1] = level_rank[record-1][1], level_rank[record][1]
              record -= 1
          player.rank = record + 1

    with open('JSONHOME/level_array.json', 'w', encoding='utf8') as dataFile:
        json.dump(level_rank, dataFile, ensure_ascii=False, indent=4)


class Rank(commands.Cog):
    def __init__(self, client):
        with open('JSONHOME/level_data.json', 'r', encoding='utf-8') as f:
            level_data = json.load(f)
        with open('JSONHOME/level_array.json', 'r', encoding='utf-8') as f:
            level_rank = json.load(f)
        self.client = client
        self.level_rank = level_rank
        self.level_data = level_data
        self.level_dict = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
          return
        id = str(message.author.id)
        user = str(message.author)
        if message.author != self.client.user:
            if id not in self.level_data.keys():
                player = levels.Player(id, user)
                self.level_dict[id] = player
            else:
                self.level_dict[id] = dict_to_class(id, self.level_data)
            self.level_dict[id].update()
            update_rank(self.level_dict[id], self.level_rank)
            self.level_data[id] = self.level_dict[id].__jsonencode__()
            with open('JSONHOME/level_data.json', 'w', encoding='utf-8') as f:
                json.dump(self.level_data, f, ensure_ascii=False, indent=4,
                            cls=levels.AdvencedJSONEncoder)

    @commands.command()
    async def rank(self, ctx):
        user = ctx.author
        id = str(user.id)
        player = self.level_dict[id]
        embed = EMBED.Embed()
        embed.add('user',user, True)
        embed.add(name="level", value=player.level, inline=True)
        embed.add(name="rank", value=player.rank, inline=True)
        embed.add(
            name="exp", value=f"{player.exp}/{player.ranklimit}", inline=False)
        embed = embed.output()
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Rank(client))
