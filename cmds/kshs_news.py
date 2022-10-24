from pydoc import describe
import nextcord
from nextcord.ext import commands, tasks
from core.classes import Cog_Extention
from MODULE.EMBED import Embed 

import datetime
from bs4 import BeautifulSoup
import requests
import json
from markdownify import markdownify as md
from copy import deepcopy


def get_data() -> list:
    url = "https://www.kshs.kh.edu.tw/view/index.php?WebID=269&MainType=101&SubType=0&MainMenuId=28016&SubMenuId=0&NowMainId=28016&NowSubId=0"
    r = requests.get(url)
    kshs_url = "https://www.kshs.kh.edu.tw/view/"
    soup = BeautifulSoup(r.text, 'lxml')

    tags = soup.select('.ContentList > div > a')

    data = []

    for tag in tags:
        urls = tag['href'][10:]
        post = dict(i.split("=") for i in urls.split("&"))
        post['title'] = tag.text
                
        post['url'] = kshs_url + tag['href']
        url = post['url']
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        tags = soup.select('.ContentBody')
        post['content'] = md(tags[0].__str__())
        data.append(post)
    
    data = sorted(data, key= lambda x: x['DataId'], reverse=True)  
    return data


def read_last_post():
    with open('JSONHOME/kshs_news.json', 'r', encoding='utf-8') as f:
        last_data = json.load(f)
        return last_data[0] 
 
class KshsNews(Cog_Extention):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.my_background_task.start()

    @tasks.loop(hours=1)
    async def my_background_task(self):
        data = get_data()
        last_post = read_last_post() 
        index = data.index(last_post) 
        new_posts = deepcopy(data)[:index] if index != -1 else data
        for post in new_posts:
            url = post['url']
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            tags = soup.select('.ContentBody')
            post['content'] = md(tags[0].__str__())
            print(post['content'])
            
        
        for post in new_posts:
            embed = Embed()      
            embed.add(name=post['title'] or "WTF", value=post['content'][:1020], inline=False)
        
            channel = self.client.get_channel(855453245202628618)
            await channel.send(embed=embed.output()) 
        
        with open('JSONHOME/kshs_news.json', 'w', encoding='utf8') as dataFile:
            json.dump(data, dataFile, ensure_ascii=False, indent=4)
            
    @my_background_task.before_loop
    async def before_my_task(self):
        await self.client.wait_until_ready()  # wait until the bot logs in  
 
def setup(client):
    client.add_cog(KshsNews(client))