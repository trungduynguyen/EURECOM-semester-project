# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 12:51:45 2017

@author: Trung Duy
"""

import os
from selenium import webdriver
from bs4 import BeautifulSoup
from requests import get
import datetime as dtime
import time
from itertools import islice
from lxml import etree as ET
from unidecode import unidecode
import random as rand


alllink = []
recipelinks = []
inputfile = open('recipe_list.txt','r')
#recipelinks = islice(inputfile,50)
#for n in range(0,len(inputfile)):
#    recipelinks.append(inputfile.readline())
#with open('recipe_list.txt','r') as f:
#    for n in range(1000,51000):
#        recipelinks.append(f.readlines()[n])
#for line in inputfile:
alllink = inputfile.readlines()

recipelinks = alllink[1000:51000]


for i in range(0,len(recipelinks)/500):

    Dataset = ET.Element('Dataset')
    k = 1
    for link in recipelinks[i*500: (i+1)*500]:
        link.strip('\n')
        browser = webdriver.Chrome()
        browser.get(link)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        
        recipe_xml = ET.SubElement(Dataset,'recipe')
        id_xml = ET.SubElement(recipe_xml, 'recipe_ID')
        id_xml.text = str(unidecode(soup.select('button.rb-open.btn-emphasis')[0].get('data-recipe-id')))
        
        category_xml = ET.SubElement(recipe_xml, 'category')
        category_xml.text = str(unidecode(soup.select('div.breadcrumbs.recipe-breadcrumbs.fd-container a')[2].getText()))
        
        link_xml = ET.SubElement(recipe_xml, 'link')
        link_xml.text =  link
        
        name_xml = ET.SubElement(recipe_xml, 'recipe_name')
        name_xml.text = str(unidecode(soup.select('header.recipe.fd-recipe h1')[0].getText()))
        
        rate_xml = ET.SubElement(recipe_xml, 'rate')
        rate_xml.text = str(unidecode(soup.select('span.fd-rating-percent span')[0].getText()))
        
        vote_xml = ET.SubElement(recipe_xml, 'vote')
        vote_xml.text = str(soup.select('a.af-show-reviews.af-review-count')[0].getText()).translate(None,"()")
        
        cook_time_xml = ET.SubElement(recipe_xml,'cook_time')
        cook_time_xml.text = str(soup.select('div.recipe-cooktime')[0].getText()).translate(None,"\n ").replace('READYIN:','')
        
        serving_xml = ET.SubElement(recipe_xml,'serving')
        serving_xml.text = str(soup.select('span.count')[0].getText())
        
        
        list_ingredient = soup.select('ul.ingredient-list li')
        list_ingredient_xml = ET.SubElement(recipe_xml,'list_ingredient') 
        for li in list_ingredient:
            ingredient = ET.SubElement(list_ingredient_xml,'ingredient')
            ingredient.text = str(unidecode(li.getText()))
        
        
        
        list_direction = soup.select('ol.expanded li',)
        list_direction_xml = ET.SubElement(recipe_xml,'list_direction') 
        for li in list_direction[:-1]:
            direction = ET.SubElement(list_direction_xml,'direction')
            direction.text = str(unidecode(li.getText()))
        
        
        print('Loading . . . . . . . . . ' + str(float((k*100)/500))+'%')
        k+=1
        browser.close()
        browser.quit()
    
    
    obj = ET.tostring(Dataset, pretty_print=True, xml_declaration=True)
    output = open('./data/output_'+ str(i) +'.xml','w')
    output.write(obj)
    output.close()
    
    sleep_time = rand.randint(120, 300)
    print('\n====================================\nFinnish output ' + str(i) + ' - Sleep time ' + str(sleep_time) + ' seconds\n====================================\n')
    time.sleep(sleep_time)

    

