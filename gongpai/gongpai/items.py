# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GongpaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_id = scrapy.Field()
    bid_id = scrapy.Field()
    title = scrapy.Field()
    bid_status = scrapy.Field()
    applyCount = scrapy.Field()
    viewerCount = scrapy.Field()
    bidCount = scrapy.Field()
    itemUrl = scrapy.Field()
    dealPrice = scrapy.Field()
    evaluatePrice = scrapy.Field()
    deal_time = scrapy.Field()
    deal_status = scrapy.Field()
    start_price = scrapy.Field()
    delay_count = scrapy.Field()
    court = scrapy.Field()
    contact = scrapy.Field()
    phone_num = scrapy.Field()
    limit_status = scrapy.Field()
    remind_count = scrapy.Field()
    img_url = scrapy.Field()
    data_from = scrapy.Field()
    coordinate = scrapy.Field()
    latitude = scrapy.Field()
    longtitude = scrapy.Field()

    confidence = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    town = scrapy.Field()
    detailAdrress = scrapy.Field()
    detail_desc = scrapy.Field()
    detail_url = scrapy.Field()
    crawled_time = scrapy.Field()
    spider = scrapy.Field()
