import requests
import pandas as pd
import json,os,collections
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from tqdm import tqdm

driver = webdriver.Chrome()

def getData(website):
    #website = "https://whop.com/marketplace/boa/"
    driver.get(website)
    title=driver.find_element(By.XPATH,"//h1").text
    ratings=driver.find_element(By.XPATH,"//div[contains(@class, 'subtitle3 text-whop-black')]").text
    reviews=driver.find_element(By.XPATH,"//div[contains(@class,'text-whop-dark-gray text3 cursor-pointer underline')]").text
    num_reviews = int(reviews.split('(')[-1].split(' ')[0])
    el = driver.find_element('xpath','//div[@class="mb-6 space-y-2"]')
    description = [x.text.strip() for x in el.find_elements('xpath','.//*')]
    description = [x for x in description if x not in ['','Show more']]
    description = description[0].split('\n')
    Boxes=driver.find_elements(By.XPATH,"//div[contains(@class, 'border-t-whop-stroke')]")
    #Boxes[0].find_elements('xpath','.//div[contains(@class,"font-display")]')[0].text
    els = Boxes[0].find_elements('xpath','.//div[contains(@class,"flex gap-6")]//div[@class="text-header4"]')
    titles= [x.text for x in els]
    els = Boxes[0].find_elements('xpath','.//div[contains(@class,"flex gap-6")]//div[@class="text-paragraph2 text-whop-dark-gray"]')
    parags = [x.text for x in els]
    feature_box_data = {k:v for k,v in zip(titles,parags)}
    els = Boxes[-2].find_elements('xpath','.//p[@class="text-paragraph2 whitespace-nowrap"]')
    about_seller = [x.text for x in els]
    desc = Boxes[-2].find_elements('xpath','.//div[@class="text-paragraph2 text-whop-black whitespace-pre-wrap"]')[0].text
    about_seller.append(desc)
    social_data = []
    socials = Boxes[-2].find_elements('xpath','.//div[@class="border-whop-stroke flex justify-between border-b-[0.5px] py-4"]')
    for social in socials:
        website = social.find_element('xpath','.//div[@class="text-text3"]').text
        website_link = social.find_element('xpath','.//a[@class="text-whop-field-highlight flex cursor-pointer items-center gap-0.5"]').get_attribute('href')
        social_data.append([website,website_link])
    return [title,ratings,num_reviews,description,feature_box_data,about_seller,social_data]


website_list = []
for i in tqdm(range(1,204)):
    url = f"https://whop.com/search/?query=&page={i}"
    driver.get(url)
    els = driver.find_elements('xpath','//a[@target="_blank"]')
    websites = [x.get_attribute('href') for x in els]
    websites = [x for x in websites if x.find('/marketplace/')!=-1]
    website_list+=websites
website_list=list(set(website_list))
full_webdata = []
for website in tqdm(website_list):
    web_data  = getData(website)
    full_webdata.append(web_data)
df = pd.DataFrame(full_webdata)
df.to_csv('Data.csv',index=False)