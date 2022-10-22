import requests
import time
import pandas as pd
import random
import numpy as np

from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from datetime import datetime
from os import listdir, system


def makeInfo(cnt):
    res = {
        "종목코드": [],
        "상장주식수": [],
        "외국인한도주식수": [],
        "외국인보유주식수": [],
        "EPS": [],
        "추정EPS": [],
        "BPS": [],
        "배당수익률": [],
        "동일업종 PER": []
    }
    codes = pd.read_csv("kospi.csv")["종목코드"]
    for code in tqdm(codes[:cnt]):
        code = str(code)

        cols = pd.DataFrame(res).columns

        url = "https://finance.naver.com/item/main.nhn?code=" + code
        response = requests.get(url)
        html = bs(response.text, 'html.parser')
        try:
            info = html.select("div[id=tab_con1]")[0]
        except:
            print("정보 없음")
            return

        lstocks = info.select("tr")
        s = set(cols[1:])
        for tr in lstocks:
            th = tr.select("th")[0]
            for c in s:
                if c in th.text:
                    try:
                        td = tr.select("td em")[-1]
                        data = td.text.replace(",", "").replace("%", "")
                        data = np.nan if data == "N/A" else float(data)
                        res[c].append(data)
                        s.remove(c)
                        break
                    except:
                        pass
        for c in s:
            res[c].append(np.nan)
        res["종목코드"].append(code)
        time.sleep(random.uniform(0.5, 1))

    df = pd.DataFrame(res)
    df.to_csv("kospi_info.csv")


makeInfo(int(input("코스피 시가총액 상위 N개 정보: ")))