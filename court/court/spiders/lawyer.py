# -*- coding: utf-8 -*-
import logging

import requests
import scrapy
from copy import deepcopy

from court.items import CourtItem

from proxy import *

logger = logging.getLogger("court_info")


class LawyerSpider(scrapy.Spider):

    name = 'lawyer'
    allowed_domains = ['www.lawtime.cn']
    start_urls = ['http://www.lawtime.cn/fayuan/']



    def parse(self, response):
        item = CourtItem()
        # 获取所有省的法院链接地址
        logger.info('info on %s', response.url)
        logger.warning('WARNING on %s', response.url)
        logger.debug('info on %s', response.url)
        logger.error('info on %s', response.url)

        # 获取所有省的的url链接
        provice_list = response.xpath("//div[@class='warp2']//div[@class='trends']//p//a/@href").extract()
        # print(provice_list)

        if provice_list:
            for provice in provice_list[4:]:
                item["province_url"] = provice.strip()
                yield scrapy.Request(
                    item["province_url"], callback=self.get_city_url, meta={"item":deepcopy(item)}
                )

            for city in provice_list[:4]:
                item["city_url"] = city.strip()
                yield scrapy.Request(
                    item["city_url"], callback=self.get_court_url,meta={"item":deepcopy(item)}
                )

    #获取直辖市的url链接
    def get_city_url(self, response):
        item = response.meta["item"]
        city_list = response.xpath("//div[@class='midarea ma2']//div[@class='mcol']//span[@class='right']/a/@href").extract()
        # print(city_list)
        # 遍历所有市,找出所有县的url
        for city in city_list:
            item["city_url"] = city.strip()
            print(item["city_url"])
            yield scrapy.Request(
                item["city_url"], callback=self.get_court_url, dont_filter=True,meta={"item":deepcopy(item)}
            )

    #获取法院详细信息
    def get_court_url(self,response):
        item = response.meta["item"]
        #法院信息列表
        court_list = response.xpath("//div[@class='midarea ma2']//div[@class='mcol']//dl").extract()
        # 遍历所有市,找出所有县的url
        # print(court_list)
        for court in court_list:
            # print(court)
            item["court"] = court.xpath(".//dt[@class='mccname']/text()").extract_first()
            print(item["court"])
            item["phone_num"] = court.xpath(".//dd[2]/text()").extract_first()
            item["address"] = court.xpath(".//dd[3]/text()").extract_first()
            print(item)
            yield item
        #下一页
        # first_url = response.xpath("//div[@class='mcpage c0165B8']//p/a[last()]/@href").extract_first()
        next_url = response.xpath("//a[contains(.,'下一页')]/@href").extract_first()
        if next_url:
            yield scrapy.Request(
                next_url,callback=self.get_court_url
            )


