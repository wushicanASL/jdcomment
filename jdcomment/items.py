# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field
import scrapy

class JdcommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=Field()
    userProvince=Field()
    comments=Field()
    commtime = Field()
    prosize_col=Field()
    level = Field()
    mobile = Field()