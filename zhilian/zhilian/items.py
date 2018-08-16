# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst
from scrapy.loader import ItemLoader

class ZhilianItemLoader(ItemLoader):

    default_output_processor = TakeFirst()

class ZhilianItem(scrapy.Item):

    title = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()