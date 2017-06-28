# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 13:21:02 2017

@author: Trung Duy
"""

from lxml import etree as ET
#from unidecode import unidecode
import string
import re
from nltk import ngrams
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import pandas as pd
import numpy as np



def process_string(text):
    table = string.maketrans("","")
    res = []
    
    new_text = text.translate(table,string.punctuation)
    
    for i in range(1,len(new_text)):
        igrams = ngrams(new_text.split(), i)
        for grams in igrams:
            token = ''
            for n in range(0,i):
                token += grams[n]+ ' '
                
            lemma_tok = lemmatize_sentence(token)
            res.append(lemma_tok.rstrip().decode('utf-8','ignore'))
    return res

def lemmatize_sentence(text):
    lemmatizr = WordNetLemmatizer()
    tokens = nltk.word_tokenize(text)
    lemma_text = [lemmatizr.lemmatize(token) for token in tokens]
    
    return str(' '.join(word for word in lemma_text))


def Initial_dict(filename):
    ingredient_input = open(filename).read().splitlines()
    processed_ingredient_input = sorted(set([lemmatize_sentence(item) for item in ingredient_input]))
    ingredient_dict = dict((item,processed_ingredient_input.index(item)) for item in processed_ingredient_input)
    
    return ingredient_dict
# Save
#np.save('ingredient_dict.npy', ingredient_dict) 

# Load
ingredient_dict = np.load('ingredient_dict.npy').item()



def Parse_index(text, ingredient_dict):
    ingre_idx = -1
    for item in process_string(text):
        if item in ingredient_dict:
            ingre_idx = ingredient_dict[item]
    return ingre_idx

def Parse_quantity(text):
    filter_regex = re.compile(r'[^\d.]+')
    tokens = nltk.word_tokenize(text)
    processed_quanti,sep,tail = tokens[0].partition('-')
    quanti = filter_regex.sub('',processed_quanti)
    if quanti:
        return float(quanti)
    return -1

def Get_key_value(text, ingredient_dict):
    
    key = value = -1
    key = Parse_index(text,ingredient_dict)
    value = Parse_quantity(text)
    if (key != -1 and value == -1):
        value = 0
    elif (key != -1 and value == 0):
        value = 1
    print('key:',key)
    print('value:',value)
    return key, value

############################################################################################



def Convert_to_Dataframe(path,ingredient_dict):

#    tree = ET.parse('data/new_metric_output_1.xml')
#    root = tree.getroot()
    
    tree = ET.parse(path)

    listRate = [ float(idx.text) for idx in tree.findall('.//recipe/rate')]
    
    #retrieve key at given index ith
    #ingredient_dict.keys()[ingredient_dict.values().index(3155)]
    
    recipe_data = []
    list_ingre = tree.findall('.//recipe/list_ingredient')
    for k in range(0, len(list_ingre)):
        ingre_vector = np.zeros(len(ingredient_dict))
        ingre = list_ingre[k].findall('ingredient')
        for item in ingre:
            if item.text:
                ingre_idx , quanti = Get_key_value(item.text, ingredient_dict)
                if ingre_idx != -1:
                    ingre_vector[ingre_idx] = quanti
        recipe_data.append(ingre_vector)
    
    
    columns = sorted(ingredient_dict.keys())
    listID = [ idx.text for idx in tree.findall('.//recipe/recipe_ID')]
    recipe_df = pd.DataFrame(recipe_data,columns= columns,index = listID)   
    recipe_df['rate'] = pd.Series(np.array(listRate),index =recipe_df.index)
    return recipe_df


#for i in range(0,11):
    #data = Convert_to_Dataframe('./data/new_metric_output_'+str(i)+'.xml',ingredient_dict)
    #data.to_csv('data/data'+str(i)+'.csv')