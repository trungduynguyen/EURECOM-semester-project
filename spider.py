# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 16:29:35 2017

@author: Trung Duy
"""
from bs4 import BeautifulSoup

#import requests


#page = requests.get("http://www.food.com/recipe/all/popular?pn=2")

#soup = BeautifulSoup(page.content, 'html.parser')

import os
from selenium import webdriver
from bs4 import BeautifulSoup
from requests import get
import datetime



#browser = webdriver.Chrome('C:\Users\Trung Duy\Documents\GitHub\EURECOM-semester-project\chromedriver.exe') # Instantiate a webdriver object
browser = webdriver.Chrome()
browser.get('http://www.food.com/recipe/all/popular?pn=1')



endTime = datetime.datetime.now() + datetime.timedelta(minutes=1)
print(datetime.datetime.now())
while True:
    if datetime.datetime.now() >= endTime:
        print(datetime.datetime.now())
        break
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

soup = BeautifulSoup(browser.page_source, 'html.parser')
#print(soup.prettify())
#soup.find_all('h2', class_='title')
# Makes list of links to get full image
#links = []
# This is the container of images on the main page
#recipes = soup.find_all('h2', class_='title')
#for recipe in recipes:
#    # Now assemble list to pass to requests and beautifulsoup
#    #links.append(recipe.get_attribute('href'))
#     for a in recipe.find_all('a', href=True):
#       print(a['href'])
#    

recipelinks = []
recipes = soup.select('h2.title a[href]')


for recipe in recipes:
    recipelinks.append(recipe['href'])
    #print(recipe['href'])

print(len(recipelinks))

datalinks = open("recipe_list.txt", "w")
for link in recipelinks:
    datalinks.writelines(link+'\n')
datalinks.close()
