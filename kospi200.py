import requests
import time
import pandas as pd
from tqdm import tqdm
import random

from bs4 import BeautifulSoup as bs

res = {
    "Name": [],
    "Code": []
}

for page in tqdm(range(1, 21)):
    url = "https://finance.naver.com/sise/entryJongmok.nhn?&page=" + str(page)
    response = requests.get(url)
    html = bs(response.text, 'html.parser')

    stocks = html.find_all("td", {"class": "ctg"})
    for stock in stocks:
        code = stock.select('a')[0]['href'].split('=')[1]
        res["Name"].append(stock.text)
        res["Code"].append(code)

    time.sleep(random.uniform(0.3, 0.7))

df = pd.DataFrame(res)
df.to_csv("kospi200.csv")