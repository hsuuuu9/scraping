from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import openpyxl
import random
import collections
from urllib.parse import urlparse
from sqlalchemy import create_engine
import pandas as pd
import MySQLdb

f = open('ua.txt', 'r', encoding='UTF-8')

data = f.read()

user_agent = data.split('\n')

db_path = "mysql://shuichi:V3Bty@45.32.249.213:3306/Amazon"
url_sql = urlparse(db_path)
conn = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(host = url_sql.hostname, port=url_sql.port, user = url_sql.username, password= url_sql.password, database = url_sql.path[1:]))

for i in range(len(user_agent)):
    options = webdriver.ChromeOptions()
    options.add_argument('--user-agent=' + user_agent[i])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #options.add_argument("--headless")
    options.add_experimental_option('useAutomationExtension', False)

    options.add_argument('--disable-desktop-notifications')
    options.add_argument("--disable-extensions")
    options.add_argument('--lang=ja')

    driver = webdriver.Chrome(options=options)
    stealth(driver,
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
    )
    driver.get('https://twitter.com/600k_labo')
    time.sleep(2)
    try:
        element = driver.find_element_by_class_name('errorContainer')
    except:
        le= 'select * from twitter.useragent where ua ="'+user_agent[i]+'";'
        df = pd.read_sql(le, conn)
        if len(df) == 0:
            letter = 'insert into twitter.useragent values("'+user_agent[i]+'")'
            try:
                conn.execute(letter)
            except:
                print('error')
    driver.quit()
