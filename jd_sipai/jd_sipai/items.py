# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdSipaiItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    next_url = scrapy.Field()
    page_url = scrapy.Field()

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
    house_useage_detail = scrapy.Field()

    detail_url = scrapy.Field()
    crawled_time = scrapy.Field()
    spider = scrapy.Field()
    court_url = scrapy.Field()

    bid_record_url = scrapy.Field()
    view_url = scrapy.Field()
    displayStatus = scrapy.Field()
    bid_record_time = scrapy.Field()
    bid_record_price = scrapy.Field()
    bid_record_status = scrapy.Field()
    detail_record_url = scrapy.Field()

    paimaiId = scrapy.Field()
    vendorId = scrapy.Field()
    albumId = scrapy.Field()
    skuId = scrapy.Field()
    create_time = scrapy.Field()
    edit_time = scrapy.Field()

    pid = scrapy.Field()
    paimai_detail_url = scrapy.Field()
    bid_code = scrapy.Field()
