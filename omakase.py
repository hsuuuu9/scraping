from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN
import time
import re
import openpyxl
import random
from joblib import Parallel, delayed
import collections
from urllib.parse import urlparse
from sqlalchemy import create_engine
import pandas as pd
import MySQLdb
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
'''options.add_argument('--no-sandbox')
options.add_argument('--headless')'''
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
stealth(driver,
vendor="Google Inc.",
platform="Win32",
webgl_vendor="Intel Inc.",
renderer="Intel Iris OpenGL Engine",
fix_hairline=True,
)
db_path = "mysql://omakase"
url_sql = urlparse(db_path)
conn = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(host = url_sql.hostname, port=url_sql.port, user = url_sql.username, password= url_sql.password, database = url_sql.path[1:]))
le = 'select * from omakase.name;'
df = pd.read_sql(le,conn)
number_list = [n for n in range(122)]
random.shuffle(number_list)
for i in range(50):
    n = number_list[i]
    time.sleep(4)
    store_code = df['id'][n]
    ok = int(df['OK'][n])
    ng = int(df['NG'][n])
    url = 'https://omakase.in/ja/r/' + store_code
    driver.get(url)
    flag = False
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"p-r_reserve_action_reserve")))
            tf_check = driver.find_element_by_class_name('p-r_reserve_action_reserve')
            flag = True
            break
        except:
            pass
    if flag:
        if '???????????????????????????' in tf_check.text:
            ok += 1
            letter = 'UPDATE omakase.name set OK = '+str(ok)+' where id = "' + store_code + '"'
            conn.execute(letter)
        if '???????????????????????????????????????' in tf_check.text:
            ng += 1
            letter = 'UPDATE omakase.name set NG = '+str(ng)+' where id = "' + store_code + '"'
            conn.execute(letter)
import json

t = datetime.datetime.now()
fname = "cc.json"
with open(fname, "w", encoding="utf-8") as f:
    f.write(str(t.strftime('%Y-%m-%d %H:%M:%S')))
