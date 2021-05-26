from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import random
import collections
from urllib.parse import urlparse
from sqlalchemy import create_engine
import pandas as pd
import MySQLdb

db_path = "mysql://twitter"
url_sql = urlparse(db_path)
conn = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(host = url_sql.hostname, port=url_sql.port, user = url_sql.username, password= url_sql.password, database = url_sql.path[1:]))

letter_ua = 'select * from twitter.useragent'
df_ua = pd.read_sql(letter_ua, conn)
user_agent = df_ua['ua'][random.randint(0, len(df_ua))]

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-desktop-notifications')
options.add_argument("--disable-extensions")
options.add_argument('--user-agent=' + user_agent)
options.add_argument('--no-sandbox')
#options.add_argument('--headless')
options.add_argument('--lang=ja')
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(options=options)
stealth(driver,
vendor="Google Inc.",
platform="Win32",
webgl_vendor="Intel Inc.",
renderer="Intel Iris OpenGL Engine",
fix_hairline=True,
)

driver.get('https://nikkeiyosoku.com/nikkei_forecast/daily/')

element = element = driver.find_element_by_class_name("forecast-today-txt")

element.text

letter = element.text

letter =letter[:6]

le = letter[:2] + letter[3:]

money = round(int(le), -2)

driver.get('http://sxi2021.market-price-forecast.com/forecast.php')
time.sleep(random.random()*3)
driver.find_element_by_id('accountid').send_keys('278.wa.4sjdt2v@gmail.com')
time.sleep(random.random()*3)
driver.find_element_by_id('password').send_keys('Shuichi47')
time.sleep(random.random()*3)
driver.find_element_by_id('login').click()
time.sleep(random.random()*3)
driver.find_element_by_class_name('yen').send_keys(money)
time.sleep(random.random()*3)
driver.find_element_by_class_name('submit').click()
time.sleep(random.random()*3)
driver.find_element_by_class_name('ui-dialog-buttonset').click()
time.sleep(random.random()*3)
driver.quit()
