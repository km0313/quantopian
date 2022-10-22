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

page = 1
while True:
    url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page=" + \
        str(page)
    response = requests.get(url)
    html = bs(response.text, 'html.parser')

    trs = html.find_all("tr", {"onmouseover": "mouseOver(this)"})
    if len(trs) == 0:
        print("Done")
        break
    for tr in trs:
        try:
            info = tr.select("a")[0]
            res["Name"].append(info.text)
            res["Code"].append(info["href"].split("=")[1])
        except:
            pass

    print("page", page, "done")
    page += 1

df = pd.DataFrame(res)
df.to_csv("kospi.csv")