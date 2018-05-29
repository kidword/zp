# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaopingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    zwmc = scrapy.Field()
    gsmc = scrapy.Field()
    zwyx = scrapy.Field()
    gzdd = scrapy.Field()
    zwyq = scrapy.Field()
    keywords = scrapy.Field()
