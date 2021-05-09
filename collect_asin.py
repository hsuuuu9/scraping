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

db_path = "mysql://shuichi:V3Bty@45.32.249.213:3306/twitter"
url_sql = urlparse(db_path)
conn = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(host = url_sql.hostname, port=url_sql.port, user = url_sql.username, password= url_sql.password, database = url_sql.path[1:]))

letter_ua = 'select * from twitter.useragent'
df_ua = pd.read_sql(letter_ua, conn)
user_agent = df_ua['ua'][random.randint(0, len(df))]

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-desktop-notifications')
options.add_argument("--disable-extensions")
options.add_argument('--user-agent=' + user_agent)
options.add_argument('--no-sandbox')
options.add_argument('--headless')
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

db_path = "mysql://shuichi:V3Bty@45.32.249.213:3306/Amazon"
url_sql = urlparse(db_path)
conn = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(host = url_sql.hostname, port=url_sql.port, user = url_sql.username, password= url_sql.password, database = url_sql.path[1:]))

letter = 'select * from Amazon.freebooks;'
df = pd.read_sql(letter, conn)

count = 0

for i in range(len(df)):
    product = df['asin'][i]
    check_flag = df['check_flag'][i]
    if check_flag == 0:
        url = 'https://www.amazon.co.jp/dp/' + product
        driver.get(url)
        series_flag = True
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID,"series-childAsin-item_1")))
            series_flag = False
        except:
            pass
        if series_flag:
            count += 1
            p = 0
            while True:
                try:
                    frames = driver.find_elements_by_css_selector('.a-section.a-spacing-large.bucket')
                    max_page = int(frames[0].find_element_by_class_name('a-carousel-page-max').text) - 1
                    break
                except:
                    driver.execute_script("window.scrollTo(0, "+str(p*200)+");")
                    p += 1
                    time.sleep(0.5)
                    if p > 25:
                        max_page = 0
                        break

            for i in range(max_page):
                while True:
                    try:
                        go_next = frames[0].find_element_by_css_selector('.a-icon.a-icon-next')
                        go_next.click()
                        break
                    except:
                        driver.execute_script("window.scrollTo(0, "+str(p*200)+");")
                        p += 1
                        time.sleep(0.5)
                        if p > 25:
                            max_page = 0
                            break
                time.sleep(2)
                cards = frames[0].find_elements_by_class_name('a-carousel-card')
                for card in cards:
                    moneys = card.find_elements_by_css_selector('.a-size-base.a-color-price')
                    if len(moneys) == 2:
                        price = int(re.sub(r"\D", "", moneys[0].text))
                        point = int(re.sub(r"\D", "", moneys[1].text))
                        if price == point:
                            atag = card.find_element_by_class_name('a-link-normal')
                            url = atag.get_attribute('href')
                            place = url.find('pd_rd_i=')
                            new_asin = url[place+8:place+18]
                            letter = 'select * from Amazon.freebooks where asin = "'+new_asin+'"'
                            df_new = pd.read_sql(letter, conn)
                            if len(df_new)==0:
                                letter = 'insert into Amazon.freebooks values("'+new_asin+'",FALSE)'
                                conn.execute(letter)

            p = 0
            while True:
                try:
                    frames = driver.find_elements_by_css_selector('.a-section.a-spacing-large.bucket')
                    max_page = int(frames[1].find_element_by_class_name('a-carousel-page-max').text) - 1
                    break
                except:
                    driver.execute_script("window.scrollTo(0, "+str(p*200)+");")
                    p += 1
                    time.sleep(0.5)
                    if p > 25:
                        max_page = 0
                        break
            for i in range(max_page):
                while True:
                    try:
                        go_next = frames[1].find_element_by_css_selector('.a-icon.a-icon-next')
                        go_next.click()
                        break
                    except:
                        driver.execute_script("window.scrollTo(0, "+str(p*200)+");")
                        p += 1
                        time.sleep(0.5)
                        if p > 25:
                            max_page = 0
                            break
                time.sleep(2)
                cards = frames[1].find_elements_by_class_name('a-carousel-card')
                for card in cards:
                    moneys = card.find_elements_by_css_selector('.a-size-base.a-color-price')
                    if len(moneys) == 2:
                        price = int(re.sub(r"\D", "", moneys[0].text))
                        point = int(re.sub(r"\D", "", moneys[1].text))
                        if price == point:
                            atag = card.find_element_by_class_name('a-link-normal')
                            url = atag.get_attribute('href')
                            place = url.find('pd_rd_i=')
                            new_asin = url[place+8:place+18]
                            letter = 'select * from Amazon.freebooks where asin = "'+new_asin+'"'
                            df_new = pd.read_sql(letter, conn)
                            if len(df_new)==0:
                                letter = 'insert into Amazon.freebooks values("'+new_asin+'",FALSE)'
                                conn.execute(letter)
            letter = 'update Amazon.freebooks set check_flag = TRUE where asin = "'+product+'"'
            conn.execute(letter)
        else:
            letter='delete from Amazon.freebooks where asin = "'+product+'"'
            conn.execute(letter)
    if count > 4:
        break
driver.quit()
