# -*- coding: utf-8 -*-
import json
import re
import uuid

import requests
import scrapy
# from scrapy.log import logger
import logging

from copy import deepcopy

from datetime import date
import time
from scrapy_redis.spiders import RedisSpider
from scrapy.dupefilters import RFPDupeFilter
from coordinate import get_latlng

logger = logging.getLogger("jd_info")

from jd_sipai.items import JdSipaiItem
# class JdBidSpider(scrapy.Spider):
class JdBidSpider(RedisSpider):
    name = 'jd_bid_over'
    allowed_domains = ['jd.com','auction.jd.com']
    redis_key = 'JdBidSpider:start_urls'
    # start_urls = ['https://auction.jd.com/getJudicatureList.html?callback=jQuery5223987&page=1&limit=40&_=1526613080129']
    # start_urls = ['https://auction.jd.com/sifa_list.html']

    def parse(self, response):
        # 添加日志信息
        logger.info('info on %s', response.url)
        logger.warning('WARNING on %s', response.url)
        logger.debug('info on %s', response.url)
        logger.error('info on %s', response.url)

        item = JdSipaiItem()
        # item = {}

        pattern = re.search(r'"ls":(.*?),"total"',response.body.decode())
        # print(pattern)
        # if pattern:
        json_content = json.loads(pattern.group(1))
        pattern_list = list(json_content)
        for content in pattern_list:
            item["item_id"] = str(content["id"])
            # print("*****",item["item_id"])
            item["itemUrl"] = "https://paimai.jd.com/" + item["item_id"]
            item["dealPrice"] = content["currentPriceStr"]
            deal_time = content["endTime"]
            timeArray = time.localtime(deal_time/1000)  # 将毫秒转化为当前时间格式
            item["deal_time"] = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            yield scrapy.Request(
                item["itemUrl"],
                callback=self.parse_detail_url,
                meta={"item":deepcopy(item)}
            )

        #下一页

        next_url_list_temp = "https://auction.jd.com/getJudicatureList.html?callback=jQuery5223987&page={}&limit=40&_=1526613080129"
        pattern1 = re.search(r'"total":(.*?)}', response.body.decode())
        # print(pattern1)
        total_num = json.loads(pattern1.group(1))
        page_num = total_num//40 + (total_num%40 + 39)//40
        # page_num = 3
        item = {}
        for i in range(2, page_num + 1):
            item["page_url"] = next_url_list_temp.format(i)
            # print(item["page_url"])

            yield scrapy.Request(
                item["page_url"],
                callback=self.parse
            )



    def parse_detail_url(self,response):
        item = response.meta["item"]
        # print(111,item["item_id"])
        # div_list = response.xpath("//div[@class='pm-stage fn-clear']")
        title  = response.xpath("//div[@class='pm-stage fn-clear']//h1/text()").extract_first().strip()
        # 拍卖次数与标的物名称分离
        title_status = title.split("【")[-1].split("】")[0] if title else None
        if title_status == '第一次拍卖':
            item["bid_status"] = '01'
        elif title_status == '第二次拍卖':
            item["bid_status"] = '02'
        elif title_status == '第三次拍卖':
            item["bid_status"] = '03'
        elif (title_status == '重新拍卖') or (title_status == '再次拍卖'):
            item["bid_status"] = '04'
        elif title_status == '变卖':
            item["bid_status"] = '05'
        # print(item["bid_status"])
        item["title"] = title.split("【")[-1].split("】")[-1].strip() if title else None
        if item["title"]:
            confidence, lat, lng = get_latlng(item["title"])
            item["confidence"] = confidence
            item["longtitude"] = lng
            item["latitude"] = lat
            item["coordinate"] = str(lng) + ',' + str(lat)

        # 生成唯一标识的uuid信息
        u = uuid.uuid5(uuid.NAMESPACE_OID, item["title"])
        # 生成12位的整数数字
        item["bid_id"] = u.time_low
        item["data_from"] = 'https://auction.jd.com'
        item["create_time"] = date.today()
        item["edit_time"] = date.today()

        # div_list2 = response.xpath('//div[@class="pm-support"]//input[@id="consultName"]//@value')
        item["contact"] = response.xpath('//div[@class="pm-support"]//input[@id="consultName"]//@value').extract_first()
        item["phone_num"] = response.xpath('//div[@class="pm-support"]//input[@id="consultTel"]//@value').extract_first()
        # item["deal_time"] = response.xpath('//div[@class="pm-support"]//input[@id="endTime"]//@value').extract_first()
        start_price = response.xpath("//div[@class='pm-attachment']//ul/li[@class='fore1'][2]//em/text()").extract_first()


        item["start_price"] = start_price.split('¥')[1].strip() if start_price else None
        evaluateprice = response.xpath("//div[@class='pm-attachment']//ul/li[@class='fore3']//em/text()").extract_first()
        item["evaluatePrice"] = evaluateprice.split('¥')[1] if evaluateprice else None
        # print(item["contact"])
        # print(item["phone_num"])
        address = response.xpath('//div[@class="pm-sub"]//em[@id="paimaiAddress"]/text()').extract_first()
        if address:
            ls = address.split(" ")
            item["province"] = ls[0]
            item["city"] = ls[1]
            item["town"] = ls[2] if len(address) > 3 else None
            item["detailAdrress"] = ls[3] if len(address) > 3 else ls[2]

        limit_status_temp = response.xpath('//div[@class="p-flag"]//span//text()').extract_first()
        if limit_status_temp:
            item["limit_status"] = '02'
        else:
            item["limit_status"] = '01'

        #图片地址
        img_url_temp = response.xpath('//div[@id="spec-n1"]//img/@src').extract_first()
        item["img_url"] = 'http:' + img_url_temp if img_url_temp else None

        #拍卖记录的url
        # item["paimaiId"] = response.xpath('//div[@class="pm-support"]//input[@id="paimaiId"]//@value').extract_first()
        item["vendorId"] = response.xpath('//div[@class="pm-support"]//input[@id="vendorId"]//@value').extract_first()
        item["albumId"] = response.xpath('//div[@class="pm-support"]//input[@id="albumId"]//@value').extract_first()
        item["skuId"] = response.xpath('//div[@class="pm-support"]//input[@id="skuId"]//@value').extract_first()
        item["bid_record_url"] = "https://paimai.jd.com/json/current/englishquery?paimaiId={}&start=0&end=9".format(item["item_id"])
        yield scrapy.Request(
            url = item["bid_record_url"],
            callback=self.parse_bid_record_url,
            meta={"item":deepcopy(item)}
        )



    #解析相应中拍卖记录的次数，构造详情拍卖记录的列表
    def parse_bid_record_url(self,response):
        item = response.meta["item"]
        # print(222, item["item_id"])
        text1 = response.text
        # print(text1)
        json_text1 = json.loads(text1)
        if json_text1:
            text1_dict = dict(json_text1)
            #首先查看拍卖次数有没有大于１０次（下角表是０－９）
            if "bidCount" in text1_dict.keys():
                item["bidCount"] = str(text1_dict["bidCount"])
                item["delay_count"] = str(text1_dict["delayedCount"])
                auctionStatus = str(text1_dict["auctionStatus"])
                displayStatus = str(text1_dict["displayStatus"])

                #拍卖状态　00预告　01成交　02流拍,03撤销,04中止,05正在进行
                """
                "auctionStatus":"0" 预告
                auctionStatus":"1" 进行中
                auctionStatus =2 结束
                    "displayStatus":1," 成交
                    displayStatus":7 终止
                    "displayStatus":6 暂缓
                    "displayStatus":5 撤回
                """
                if auctionStatus == '0':
                    item["deal_status"] = '00'
                elif auctionStatus == '1':
                    item["deal_status"] = '05'
                elif auctionStatus == '2':
                    if displayStatus == '1':
                        item["deal_status"] = '01'
                    if displayStatus == '6':
                        item["deal_status"] = '02'
                    if displayStatus == '5':
                        item["deal_status"] = '03'
                    if displayStatus == '7':
                        item["deal_status"] = '04'


            else:
                item["bidCount"] = None

            item["view_url"] = "https://paimai.jd.com/json/ensure/queryAccess?&paimaiId={}".format(item["item_id"])
            # print("***"*10)
            # print(item["view_url"],item["item_id"])
            yield scrapy.Request(
                url=item["view_url"],
                callback=self.parse_view_url,
                meta={"item": deepcopy(item)}
            )

        # 解析报名人数

    def parse_view_url(self, response):
        item = response.meta["item"]
        # print(333, item["item_id"])
        text1 = response.text
        json_text1 = json.loads(text1)
        # print(type
        if json_text1:
            text1_dict = dict(json_text1)
            if "accessEnsureNum" in text1_dict.keys():
                item["applyCount"] = text1_dict["accessEnsureNum"]
                item["viewerCount"] = text1_dict["accessNum"]
            else:
                item["applyCount"] = None
                item["viewerCount"] = None
                # print(item["applyCount"])
                # print(item["viewerCount"])
        item["paimai_detail_url"] = 'https://paimai.jd.com/json/paimaiProduct/productDesciption?productId={}'.format(
            item["skuId"])
        yield scrapy.Request(
            url=item["paimai_detail_url"],
            callback=self.parse_paimai_detail_url,
            meta={"item": deepcopy(item)}

        )

    def parse_paimai_detail_url(self, response):
        item = response.meta["item"]
        # print(444,item["item_id"])
        detail_desc = response.xpath("//*//text()").extract()
        if detail_desc:
            detail_desc_temp = ','.join(detail_desc).strip()
            item["detail_desc"] = re.sub('\s', '', detail_desc_temp).replace(',', '').replace('\\n', '')
            # 获取房屋用途
            detail_desc_text = re.search(r"用途.*", item["detail_desc"])
            # 获取房屋性质
            # detail_desc_text = re.search(r"性质.*",detail_desc_text1)
            if detail_desc_text:

                item["house_useage_detail"] = detail_desc_text.group(0)
            else:
                item["house_useage_detail"] = None
        else:
            item["detail_desc"] = None

        item["court_url"] = "http://paimai.jd.com/json/current/queryVendorInfo.html?vendorId={0}&albumId={1}&paimaiId={2}".format(
            item["vendorId"], item["albumId"],item["item_id"])
        # print("-------" * 20)
        # print("******", item["court_url"], item["item_id"], "******")
        # print("-------"*20)
        yield scrapy.Request(
            url=item["court_url"],
            callback=self.parse_court_url,
            meta={"item": deepcopy(item)}
        )

    # 解析法院字段()
    def parse_court_url(self, response):
        item = response.meta["item"]
        # print(555, item["item_id"])
        text1 = response.text
        # pattern = re.search(r'null\((.*?)\);', text1)
        json_text1 = json.loads(text1)
        # print(item["court_url"])
        if json_text1:
            text1_dict = dict(json_text1)
            # print(text1_dict)
            if "shopName" in text1_dict.keys():
                item["court"] = text1_dict["shopName"]
            else:
                item["court"] = None
                # print(item["court"])
                # meta = {"item": deepcopy(item)}
        yield item




        #重构所有拍卖列表的url地址
        # item["detail_record_url"] = "https://paimai.jd.com/json/current/englishquery?paimaiId={}&start=0&end={}".format(item["bid_id"],item["bidCount"] - 1)
        # yield scrapy.Request(
        #     item["detail_record_url"],
        #     callback=self.parse_detail_record_url,
        #     meta={"item":item}
        # )

    #解析详情拍卖记录
    # def parse_detail_record_url(self,response):
    #     item = response.meta["item"]
    #     text1 = requests.get(item["detail_record_url"]).text
    #     # print(text1)
    #     json_text1 = json.loads(text1)
    #     text1_dict = dict(json_text1)
    #     item["dealPrice"] = text1_dict["currentPriceStr"]
    #     # print(item["dealPrice"])
    #     item["delay_count"] = text1_dict["delayedCount"]
    #     # print(item["delay_count"])
    #     item["displayStatus"] = text1_dict["displayStatus"]
    #     if item["displayStatus"] == 1:
    #         item["deal_status"] = "01"
    #     if item["displayStatus"] == 6:
    #         item["deal_status"] = "02"
    #     if item["displayStatus"] == 5:
    #         item["deal_status"] = "03"
    #     if item["displayStatus"] == 7:
    #         item["deal_status"] = "04"
    #     # print(item["deal_status"])
    #     bidList = text1_dict["bidList"]
    #     if bidList:
    #         for bid_dict in bidList:
    #             #拍卖记录的４个字段
    #             item["paimaiId"] = bid_dict["paimaiId"]
    #             item["bid_record_time"] = bid_dict["bidTimeStr1"]
    #             item["bid_record_price"] = bid_dict["priceStr"]
    #             item["bid_code"] = bid_dict["username"]
    #             # print(item["bid_record_price"])
    #             #在json数据中查看列表中的价格与当前价格是否一致，如果一致说明是成交价格，如果不是，说明出局
    #             if item["bid_record_price"] == item["dealPrice"]:
    #                 item["bid_record_status"] = "01"
    #             else:
    #                 item["bid_record_status"] = "02"
    #
    #             # print(item["bid_record_status"])
    #             yield item




        # yield item

        # print(item)





























