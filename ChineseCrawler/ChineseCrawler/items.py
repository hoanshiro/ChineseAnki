# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChineseDictSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    word = scrapy.Field()
    sample = scrapy.Field()


class HanziiSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    word = scrapy.Field()
    pinyin = scrapy.Field()
    cn_vi = scrapy.Field()
    compound = scrapy.Field()
    def_1 = scrapy.Field()
    ex_1 = scrapy.Field()
    def_2 = scrapy.Field()
    ex_2 = scrapy.Field()
    def_3 = scrapy.Field()
    ex_3 = scrapy.Field()
