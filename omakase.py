import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from sqlalchemy import create_engine
import pandas as pd
import MySQLdb


for i in range(244):
    store_code = df['id'][i]
    ok = int(df['OK'][i])
    ng = int(df['NG'][i])
    url = 'https://omakase.in/ja/r/' + store_code
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'lxml')

    tf_check = soup.find(class_ = 'p-r_reserve_action_reserve')

    if 'このお店を予約する' in tf_check.text:
        ok += 1
        letter = 'UPDATE omakase.name set OK = '+str(ok)+' where id = "' + store_code + '"'
        conn.execute(letter)
    if 'ご予約可能な枠がありません' in tf_check.text:
        ng += 1
        letter = 'UPDATE omakase.name set NG = '+str(ng)+' where id = "' + store_code + '"'
        conn.execute(letter)
