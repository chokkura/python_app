import requests
from bs4 import BeautifulSoup

# URLからHTMLを取得します
url = "https://www.mhlw.go.jp/index.html"
response = requests.get(url)
response.encoding = response.apparent_encoding

bs = BeautifulSoup(response.text, 'html.parser')

# ニュースリストタグで囲まれた部分を抽出
tags = bs.find('ul', class_='m-listNews')

# ulタグの中のaタグを抽出します
for tag in tags:
    text = tag.text
    print(text)