from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--user-data-dir=/home/ubuntu/.config/google-chrome')#user
options.add_argument('--profile-directory=Default')
options.add_argument('--disable-desktop-notifications')
options.add_argument("--disable-extensions")
options.add_argument('--lang=ja')
options.add_argument('--blink-settings=imagesEnabled=false')
#credit = 'card'
credit = 'store'
driver = webdriver.Chrome(options=options)
stealth(driver,
vendor="Google Inc.",
platform="Win32",
webgl_vendor="Intel Inc.",
renderer="Intel Iris OpenGL Engine",
fix_hairline=True,
)


url = 'https://www.pokemoncenter-online.com/?p_cd=4521329314112'
driver.get(url)
t = False
while t == False:
    if datetime.datetime.now() > datetime.datetime(2021, 5, 1, 9, 59, 59):
        t = True
driver.refresh()
for i in range(40000):
    try:
        driver.find_element_by_class_name('add_cart_btn').click()
        break
    except:
        driver.refresh()
for i in range(4000):
    try:
        driver.find_element_by_class_name('cart').click()
        break
    except:
        pass
for i in range(4000):
    try:
        driver.find_element_by_class_name('next_step').click()
        break
    except:
        pass
for i in range(4000):
    try:
        driver.find_element_by_class_name('next_step').click()
        break
    except:
        pass
if credit == 'card':
    for i in range(4000):#credit card
        try:
            driver.find_element_by_class_name('next_step').click()
            break
        except:
            pass
if credit == 'store':
    try:
        radios = driver.find_elements_by_class_name('cvs_store')
    except:pass
    for radio in radios:
        try:
            if radio.get_attribute('disabled') == 'true':
                pass
            else:
                radio.click()
                break
        except:pass
    for i in range(4000):
        try:
            driver.find_element_by_class_name('next_step').click()
            break
        except:
            pass
for i in range(4000):
    try:
        #driver.find_element_by_class_name('finish_buy').click()
        break
    except:
        pass
driver.quit()
