# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 12:51:45 2017

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
import datetime as tm




recipelinks = []

inputfile = open('recipe_list.txt','r')

for line in inputfile:
    line.strip('\n')
    recipelinks.append(line)


browser = webdriver.Chrome()
browser.get(recipelinks[1])
print(recipelinks[1])
soup = BeautifulSoup(browser.page_source, 'html.parser')
#print(soup.prettify())

rate = str(soup.select('span.fd-rating-percent span')[0].getText())
Num_of_vote = str(soup.select('a.af-show-reviews.af-review-count')[0].getText()).translate(None,"()")
cook_time = str(soup.select('div.recipe-cooktime')[0].getText()).translate(None,"\n ").replace('READYIN:','')
serving = str(soup.select('span.count')[0].getText())

#list_ingredient = soup.select('ul.ingredient-list li')
#for li in list_ingredient:
#    print(li.find('span').getText() +'\t')
#    print(li.getText())



#list_direction = soup.select('ol.expanded li',)
#for li in list_direction:
#    print(li.getText()+'\n')



browser.quit()






