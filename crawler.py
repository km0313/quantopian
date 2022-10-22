import requests
import time
import pandas as pd
import random

from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from datetime import datetime
from os import listdir, system


def exportData(date, code):
    res = {
        'Time': [],
        'Call Price': [],
        'Ask': [],
        'Bid': [],
        'Volume': [],
    }
    df = pd.DataFrame(res)

    for page in tqdm((range(1, 41))):
        url = "https://finance.naver.com/item/sise_time.nhn?code=" + \
            code + "&thistime=" + date + "161034" + "&page=" + str(page)
        response = requests.get(url)
        html = bs(response.text, 'html.parser')

        # parse
        trList = html.find_all("tr", {"onmouseover": "mouseOver(this)"})
        for tr in trList:
            tdList = tr.find_all('td')
            if ':' not in tdList[0].text:
                if page == 1:
                    print(code, "정보 없음")
                    return 1
                break

            callTime = tdList[0].text.strip()  # 체결시각
            callPrice = int(tdList[1].text.strip().replace(',', ''))  # 체결가
            ask = int(tdList[3].text.strip().replace(',', ''))  # 매도
            bid = int(tdList[4].text.strip().replace(',', ''))  # 매수
            volume = int(tdList[5].text.strip().replace(',', ''))  # 거래량

            for col, d in zip(df.columns, [callTime, callPrice, ask, bid, volume]):
                res[col].insert(0, d)

        #time.sleep(random.uniform(0.1, 0.3))

    df = pd.DataFrame(res)
    df.to_csv(code + "/" + code + "_" + date + ".csv")
    return 0


stocks = pd.read_csv("kospi200.csv", dtype=object)
date = input("날짜 입력: (2020년 7월 17일 이면 20200717)")
cnt = 0
total = len(stocks["Code"])

for code, name in zip(stocks["Code"], stocks["Name"]):
    cnt += 1
    if code not in listdir("."):
        system("mkdir " + code)
    if code + "_" + date + ".csv" in listdir("./" + code):
        print(name + "_" + date, "already exist!", f"{cnt}/{total}")
        continue
    print(name, "Start")
    exportData(date, code)
    print(name, "Done", f"{cnt}/{total}")

    if cnt == 10:
        break