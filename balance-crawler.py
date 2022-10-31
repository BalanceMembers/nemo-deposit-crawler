from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os 

import time
import datetime
import re
import json
load_dotenv()

driver = webdriver.Chrome(executable_path="./chromedriver")
driver.get("http://balance.nemolab.co.kr:8080/login")
time.sleep(2)

# 로그인을 실행
login_box = driver.find_element(By.ID, "id")
password_box = driver.find_element(By.ID, "password")

webdriver.ActionChains(driver).send_keys_to_element(login_box, os.environ.get('ID')).send_keys(Keys.TAB).perform()
webdriver.ActionChains(driver).send_keys_to_element(password_box, os.environ.get('PASSWORD')).send_keys(Keys.ENTER).perform()

#크롤러를 통해 자료 저장
rows = driver.find_elements(By.CSS_SELECTOR, "body > div > div > div:nth-child(2) > div > div > div.panel-body > form > div > table > tbody > tr")

clients = []
    
for i in range(0, len(rows)-1):

    a_1 = rows[i].find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
    b_2 = rows[i].find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
    
    clients.append({
    "no": i+1,
    "client": a_1,
    "accessNo": b_2
    })

with open("./clients.json", 'w', encoding='UTF-8-sig') as file:
     file.write(json.dumps(clients, ensure_ascii=False))
        
from ipywidgets import IntProgress
from IPython.display import display
progress_bar = IntProgress(min=0, max=110)
display(progress_bar)  

balances = []
for i in range(1, len(rows)-1):

    driver.find_element(By.CSS_SELECTOR, "body > div > div > div:nth-child(2) > div > div > div.panel-body > form > div > table > tbody > tr:nth-child(" + str(i) + ") > td:nth-child(1)").click()
    time.sleep(2)
    
    rows = driver.find_elements(By.CSS_SELECTOR, "body > div > div > div:nth-child(2) > div > div > div.panel-body > div.table-responsive > form > table > tbody > tr")
    
    for e in rows : 
        try : 
            a = e.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            date = datetime.datetime.strptime(a,'%y.%m.%d').strftime('%Y-%m-%d')
            b = e.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
            c = e.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
            d = int(re.sub(r"[^0-9]", "", e.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text))-int(re.sub(r"[^0-9]", "", e.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text))

            balances.append({'date':date, 'content':b, 'in_charge':c, 'amount':d, 'clientId':i})
            
        except :
            time.sleep(1)
            
    progress_bar.value = i
    
    driver.back()
    time.sleep(2)
    
with open("./balances.json", 'w', encoding='UTF-8-sig') as file:
     file.write(json.dumps(balances, ensure_ascii=False))