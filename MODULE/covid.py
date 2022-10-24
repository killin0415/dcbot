import requests
from bs4 import BeautifulSoup
from MODULE import EMBED


class covid():
  def __init__(self):
    self.response=requests.get("https://www.worldometers.info/coronavirus/country/taiwan/")
    self.soup=BeautifulSoup(self.response.text,"html.parser")
    self.result=self.soup.find_all("div",attrs={"class":"maincounter-number"})

  def get_covid(self):
    msglist=["病例總數",
              "死亡人數",
              "康復人數"]
    listnum=0
    embed = EMBED.Embed()
    embed.add(name="Covid-19疫情資訊", value="臺灣目前疫情狀況",inline = False)
    for covid in self.result:
        covid[listnum]=covid.text
        embed.add(name=msglist[listnum], value=covid.text, inline=False)
        listnum=listnum+1
    embed = embed.output()
    embed.set_footer(text="請各位確實戴好口罩，可有效避免飛沫傳染，若口罩沒戴確實，甚至沒帶，不僅嚴重增加飛沫傳染機率，還可處3000~15000罰緩。")
    return embed



        