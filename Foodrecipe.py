# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import scrapy
 
class recipe_link(scrapy.Item):
    Foodname = scrapy.Field()
    url = scrapy.Field()