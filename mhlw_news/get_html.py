import requests
from datetime import datetime
from bs4 import BeautifulSoup

#厚生労働省のURL
MHLW_URL = "www.mhlw.go.jp"

# URLからHTMLを取得
url = "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryou/"
response = requests.get(url)
response.encoding = response.apparent_encoding

bs = BeautifulSoup(response.text, 'html.parser')

# m-listNewsタグで囲まれた部分を抽出
ul_tag = bs.select('ul.m-listNews')

for tag in ul_tag[0]:
    # timeタグを取得
    time_tag = tag.find("time")
    a_tag = tag.find("a")
    span_tag = tag.find("span")
    
    # time_tag
    if time_tag != -1 and a_tag != -1 and span_tag != -1:
        # datetime属性を取得, datetime型に変換
        datetime_str = time_tag["datetime"]
        datetime_obj = datetime.fromisoformat(datetime_str)

        # urlをテキストに変換し、厚生労働省のドメインと合わせる
        url = a_tag['href']
        url = MHLW_URL + url

        # タイトルを取得
        title_text = span_tag.text

        # 月日を出力
        print(datetime_obj.date())
        print(url)
        print(title_text)