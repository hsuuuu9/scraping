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
import datetime

db_path = "mysql://shuichi:V3Bty@45.32.249.213:3306/twitter"
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

all_count = 0
check_flag_sum = 0

f = open('asin_log.txt', 'a')

for i in range(len(df)):
    product = df['asin'][i]
    check_flag = df['check_flag'][i]
    check_flag_sum += check_flag
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
            price = 10000000
            point = 20000000
            count = 0
            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME,"tmm-olp-links")))
                add = driver.find_elements_by_class_name('tmm-olp-links')
            except:
                add = []
            for letters in add:
                if '獲得ポイント' in letters.text:
                    count += 1
                    WebDriverWait(letters, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".extra-message.olp-link")))
                    price_element = letters.find_element_by_css_selector(".extra-message.olp-link")
                    if "Kindle 価格" in price_element.text:
                        price = int(re.sub(r"\D", "", price_element.text))
                    WebDriverWait(letters, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".a-size-mini.a-color-secondary.extra-message")))
                    point_element = letters.find_element_by_css_selector(".a-size-mini.a-color-secondary.extra-message")
                    if "獲得ポイント" in point_element.text:
                        point = int(re.sub(r"\D", "", point_element.text))
            if count == 0 and len(add)!=0:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".a-button.a-button-selected.a-spacing-mini.a-button-toggle.format")))
                add_element = driver.find_element_by_css_selector(".a-button.a-button-selected.a-spacing-mini.a-button-toggle.format")
                try:
                    WebDriverWait(add_element, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".a-size-base.a-color-price.a-color-price")))
                    if "￥" in add_element.find_element_by_css_selector(".a-size-base.a-color-price.a-color-price").text:
                        price_element = add_element.find_element_by_css_selector(".a-size-base.a-color-price.a-color-price")
                        price = int(re.sub(r"\D", "", price_element.text))
                    WebDriverWait(add_element, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".a-color-price.a-text-normal")))
                    if "獲得ポイント" in add_element.find_element_by_css_selector(".a-color-price.a-text-normal").text:
                        point_element = add_element.find_element_by_css_selector(".a-color-price.a-text-normal")
                        point = int(re.sub(r"\D", "", point_element.text))
                except:
                    pass
            if price == point and price != 0:
                try:
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID,"productTitle")))
                    title = driver.find_element_by_id('productTitle').text
                except:
                    title = 'タイトル'
                letter='update Amazon.freebooks set title = "'+title+'" where asin = "'+product+'"'
                conn.execute(letter)
            else:
                letter='delete from Amazon.freebooks where asin = "'+product+'"'
                conn.execute(letter)
                f.write('delete:'+product+':not price'+'\n')
            all_count += 1
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
                            letter_new = 'select * from Amazon.freebooks where asin = "'+new_asin+'"'
                            df_new = pd.read_sql(letter_new, conn)
                            if len(df_new)==0:
                                letter = 'insert into Amazon.freebooks values("'+new_asin+'",FALSE,FALSE,"タイトル")'
                                conn.execute(letter)
                                f.write('append:'+new_asin+'\n')

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
                            letter_new = 'select * from Amazon.freebooks where asin = "'+new_asin+'"'
                            df_new = pd.read_sql(letter_new, conn)
                            if len(df_new)==0:
                                letter = 'insert into Amazon.freebooks values("'+new_asin+'",FALSE,FALSE,"タイトル")'
                                conn.execute(letter)
                                f.write('append:'+new_asin+'\n')
            letter = 'update Amazon.freebooks set check_flag = TRUE where asin = "'+product+'"'
            conn.execute(letter)
        else:
            letter='delete from Amazon.freebooks where asin = "'+product+'"'
            conn.execute(letter)
            f.write('delete:'+product+':series'+'\n')
    if all_count > 4:
        break

if len(df) == check_flag_sum:
    new_list = random.sample([n for n in range(len(df))], 7)
    for i in new_list:
        product = df['asin'][i]
        check_flag = 0
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
                price = 10000000
                point = 20000000
                count = 0
                try:
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME,"tmm-olp-links")))
                    add = driver.find_elements_by_class_name('tmm-olp-links')
                except:
                    add = []
                for letters in add:
                    if '獲得ポイント' in letters.text:
                        count += 1
                        WebDriverWait(letters, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".extra-message.olp-link")))
                        price_element = letters.find_element_by_css_selector(".extra-message.olp-link")
                        if "Kindle 価格" in price_element.text:
                            price = int(re.sub(r"\D", "", price_element.text))
                        WebDriverWait(letters, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".a-size-mini.a-color-secondary.extra-message")))
                        point_element = letters.find_element_by_css_selector(".a-size-mini.a-color-secondary.extra-message")
                        if "獲得ポイント" in point_element.text:
                            point = int(re.sub(r"\D", "", point_element.text))
                if count == 0 and len(add)!=0:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".a-button.a-button-selected.a-spacing-mini.a-button-toggle.format")))
                    add_element = driver.find_element_by_css_selector(".a-button.a-button-selected.a-spacing-mini.a-button-toggle.format")
                    try:
                        WebDriverWait(add_element, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".a-size-base.a-color-price.a-color-price")))
                        if "￥" in add_element.find_element_by_css_selector(".a-size-base.a-color-price.a-color-price").text:
                            price_element = add_element.find_element_by_css_selector(".a-size-base.a-color-price.a-color-price")
                            price = int(re.sub(r"\D", "", price_element.text))
                        WebDriverWait(add_element, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".a-color-price.a-text-normal")))
                        if "獲得ポイント" in add_element.find_element_by_css_selector(".a-color-price.a-text-normal").text:
                            point_element = add_element.find_element_by_css_selector(".a-color-price.a-text-normal")
                            point = int(re.sub(r"\D", "", point_element.text))
                    except:
                        pass
                if price == point and price != 0:
                    try:
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID,"productTitle")))
                        title = driver.find_element_by_id('productTitle').text
                    except:
                        title = 'タイトル'
                    letter='update Amazon.freebooks set title = "'+title+'" where asin = "'+product+'"'
                    conn.execute(letter)
                else:
                    letter='delete from Amazon.freebooks where asin = "'+product+'"'
                    conn.execute(letter)
                    f.write('delete:'+product+':not price'+'\n')
                all_count += 1
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
                                letter_new = 'select * from Amazon.freebooks where asin = "'+new_asin+'"'
                                df_new = pd.read_sql(letter_new, conn)
                                if len(df_new)==0:
                                    letter = 'insert into Amazon.freebooks values("'+new_asin+'",FALSE,FALSE,"タイトル")'
                                    conn.execute(letter)
                                    f.write('append:'+new_asin+'\n')

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
                                letter_new = 'select * from Amazon.freebooks where asin = "'+new_asin+'"'
                                df_new = pd.read_sql(letter_new, conn)
                                if len(df_new)==0:
                                    letter = 'insert into Amazon.freebooks values("'+new_asin+'",FALSE,FALSE,"タイトル")'
                                    conn.execute(letter)
                                    f.write('append:'+new_asin+'\n')
                letter = 'update Amazon.freebooks set check_flag = TRUE where asin = "'+product+'"'
                conn.execute(letter)
            else:
                letter='delete from Amazon.freebooks where asin = "'+product+'"'
                conn.execute(letter)
                f.write('delete:'+product+':series'+'\n')
        if all_count > 4:
            break
f.close()
driver.quit()

import json

t = datetime.datetime.now()
fname = "bb.json"
with open(fname, "w", encoding="utf-8") as f:
        f.write(str(t.strftime('%Y-%m-%d %H:%M:%S')))
