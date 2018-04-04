# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZfItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    descript = scrapy.Field()
    xiaoqu_name = scrapy.Field()
    xiaoqu_link = scrapy.Field()
    zone = scrapy.Field()
    meters = scrapy.Field()
    orient = scrapy.Field()
    high = scrapy.Field()
    year = scrapy.Field()
    price = scrapy.Field()
    price_update = scrapy.Field()
    location = scrapy.Field()


