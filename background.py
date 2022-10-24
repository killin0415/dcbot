import requests
import json
import bs4

from markdownify import markdownify as md
import pprint
def get_data() -> list:
    url = "https://www.kshs.kh.edu.tw/view/index.php?WebID=269&MainType=101&SubType=0&MainMenuId=28016&SubMenuId=0&NowMainId=28016&NowSubId=0"
    r = requests.get(url)
    kshs_url = "https://www.kshs.kh.edu.tw/view/"
    soup = bs4.BeautifulSoup(r.text, 'lxml')

    tags = soup.select('.ContentList > div > a')

    data = []

    for tag in tags:
        urls = tag['href'][10:]
        post = dict(i.split("=") for i in urls.split("&"))
        post['title'] = tag.text
                
        post['url'] = kshs_url + tag['href']
        url = post['url']
        r = requests.get(url)
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        tags = soup.select('.ContentBody')
        post['content'] = md(tags[0].__str__())
        data.append(post)
    
    data = sorted(data, key= lambda x: x['DataId'], reverse=True)  
    return data


def read_last_post():
    with open('JSONHOME/kshs_news.json', 'r', encoding='utf-8') as f:
        last_data = json.load(f)
        return last_data[0] if len(last_data) else {}
      
data = get_data()
post = read_last_post()

for i in post.keys():
    print(post[i] == data[0][i])
    if not post[i] == data[0][i]:
          print(i)
          print(post[i])
          print(data[0][i])

print(post == data[0])