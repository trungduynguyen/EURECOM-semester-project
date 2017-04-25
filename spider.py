# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 16:29:35 2017

@author: Trung Duy
"""
from bs4 import BeautifulSoup


#page = requests.get("http://www.food.com/recipe/all/popular?pn=2")

#soup = BeautifulSoup(page.content, 'html.parser')

import os
from selenium import webdriver
from bs4 import BeautifulSoup
from requests import get
import datetime
import time
from selenium.webdriver.common.keys import Keys
from lxml import etree as ET
import random as rand



#endTime = datetime.datetime.now() + datetime.timedelta(minutes=120)
pre_link = 'http://www.food.com/services/mobile/fdc/search/sectionfront?pn='
pos_link = '&searchTerm=&recordType=Recipe&sortBy=mostPopular&collectionId=17'
link = []

start_time = datetime.datetime.now()

#total lenght 51250, split to 4 times
for i in range(1,12813):
    browser = webdriver.Chrome()
#browser.get('http://www.food.com/recipe/all/popular?pn=1')
#print(datetime.datetime.now())

    browser.get(pre_link+str(i)+pos_link)

#while True:
#    if datetime.datetime.now() >= endTime:
#        break
#    #link = browser.find_element_by_css_selector('h2.title')
#    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
#    #browser.set_page_load_timeout(10)
#    #browser.implicitly_wait(10)
#    time.sleep(2)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.close()
    browser.quit()

    clean_html = soup.select('span.text')
    record_url = []
    for k in range(0,len(clean_html)):
        record_url.append(clean_html[k].getText())

    link = link + [str(s) for s in record_url if "http://www.food.com/recipe/" in s]
    print('Done loop ' + str(i))
    if (datetime.datetime.now().minute-start_time.minute)%9 == 1 :
        time.sleep(120)
    else:
        time.sleep(rand.randint(1, 10))


#recipelinks = []
#recipes = soup.select('h2.title a[href]')
#
#
#for recipe in recipes:
#    recipelinks.append(recipe['href'])
#    #print(recipe['href'])
#
#print(len(recipelinks))
#
datalinks = open("recipe_list.txt", "w")
for item in link:
    datalinks.writelines(item+'\n')
datalinks.close()


