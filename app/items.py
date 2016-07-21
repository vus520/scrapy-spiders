# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GoogleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    num = scrapy.Field()
    cate = scrapy.Field()
    rate = scrapy.Field()
    desc = scrapy.Field()
    meta = scrapy.Field()
    info = scrapy.Field()
    score = scrapy.Field()
    pkg = scrapy.Field()