# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CourtItem(scrapy.Item):
    # define the fields for your item here like:
    province_url = scrapy.Field()
    city_url = scrapy.Field()
    court = scrapy.Field()
    address = scrapy.Field()
    phone_num = scrapy.Field()


