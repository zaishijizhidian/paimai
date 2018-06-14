# -*- coding: utf-8 -*-
import re

import scrapy
from gongpai.items import GongpaiItem

class BidOverSpider(scrapy.Spider):
    name = 'bid_over'
    allowed_domains = ['www.gpai.net','s.gpai.net']
    start_urls = ['http://s.gpai.net/sf/search.do?restate=3&Page=1']

    def parse(self, response):
        div_list = response.xpath("//div[@class='filt-result-list']//div[@class='item-tit']//@href").extract()
        item = {}
        for item_url in div_list:
            item["item_url"] = item_url
            yield  scrapy.Request(
                item["item_url"],
                callback=self.parse_detail_url
            )

        #下一页url
        # page_num_temp = response.xpath("//span[@class='page-infos']//text()").extract_first()
        # pattern = re.search(r"共(\d+)页",page_num_temp)
        # page_num = pattern.group(1)
        # for i in range(2,int(page_num)):
        #
        #     next_url = "http://s.gpai.net/sf/search.do?restate=3&Page={}".format(i)
        #     yield scrapy.Request(
        #     next_url,
        #     callback=self.parse
        #     )


    def parse_detail_url(self,response):
        item = GongpaiItem()
        div_list1 = response.xpath("//div[@class='d-m-infos']")
        if div_list1:
            for div in div_list1:
            #网页标签由两种形式，所以要采用两种不同的形式
                title = div.xpath(".//div[@class='d-m-title']//text()").extract_first()

                item["title"] = title if title else None
                # print(item["title"])
                #网页的标签规则不统一，起始网页就是成交的，所以交易状态直接标成“成交”
                item["deal_status"] = '01'
                item["dealPrice"] = div.xpath(".//b[@class='price-red']//text()").extract_first()
                start_price = div.xpath(".//span[@id='Price_Start']//text()").extract_first()
                if start_price:
                    item["start_price"] = start_price
                #拍卖阶段
                bid_status = response.xpath("//div[@class='d-m-infos']//table[1]//tr[1]//td[2]//text()").extract_first()
                if bid_status:
                    bid_status_temp = bid_status
                    bid_status_pattern = re.search(r"拍卖次数：第(.*?)次拍卖",bid_status_temp)
                    if bid_status_pattern:
                        bdc = bid_status_pattern.group(1)
                        if bdc == "一":
                            item["bid_status"] = "01"
                        if bdc == "二":
                            item["bid_status"] = "02"
                        if bdc == "三":
                            item["bid_status"] = "03"
                    else:
                        item["bid_status"] = None
                deal_price = div.xpath(".//span[@id='Price_Start']//text()").extract_first()
                if deal_price:
                    item["evaluatePrice"] = deal_price
                court = div.xpath(".//table//td[@class='pr7']//text()").extract_first()
                if court:
                    item["court"] = court

                phone = div.xpath(".//span[@class='d-m-tel fr']//i//text()").extract_first()
                if phone:
                    item["phone_num"] = phone
                # print(item["phone_num"])
                contact = div.xpath('.//table//td[@valign="top"]//text()').extract_first()

                if contact:
                    item["contact"] = contact

        else:
            item["title"] = response.xpath("//div[@class='xq-right1']//div[@class='DivItemName']//text()").extract_first()
            start_price1 = response.xpath('//div[@class="xq-cont204"]//span[@id="Price_Start"]//text()').extract_first()
            item["start_price"] = start_price1 if start_price1 else None
            bid_status = response.xpath("//div[@class='xq-cont204']//li[4]//text()").extract_first()
            # item["bid_status"] = bid_status_temp
            if bid_status:
                bid_status_temp = bid_status
                bid_status_pattern = re.search(r"拍卖次数：第(.*?)次拍卖", bid_status_temp)
                if bid_status_pattern:
                    bdc = bid_status_pattern.group(1)
                    if bdc == "一":
                        item["bid_status"] = "01"
                    if bdc == "二":
                        item["bid_status"] = "02"
                    if bdc == "三":
                        item["bid_status"] = "03"
                else:
                    item["bid_status"] = None
            evaluatePrice = response.xpath("//div[@class='xq-right1']//div[@class='xq-cont204']//li[5]//text()").extract_first()
            evaluatePrice_temp = re.search(r"评 估 价：(.*?) 元",evaluatePrice) if evaluatePrice else None
            item["evaluatePrice"] = evaluatePrice_temp.group(1) if evaluatePrice_temp else None
            item["court"] = response.xpath("//div[@class='xq-cont204']//li[8]//text()").extract_first()
            item["phone_num"] = response.xpath("//div[@class='xq-right1']//div[@class='xq-cont202-tel']//text()").extract_first()
            item["contact"] = response.xpath("//div[@class='xq-cont204']//li[11]//text()").extract_first()
            deal_time_temp = response.xpath("//div[@class='fl']//a[2]//text()").extract_first()
            print(deal_time_temp)
            deal_time = re.search(r"[\d]+年(.*?)月(.*?)日",deal_time_temp) if deal_time_temp else None
            item["deal_time"] = deal_time.group(0).replace("年","-").replace("月","-").replace("日","") if deal_time else None
        div_list2 = response.xpath("//div[@class='peoples-infos']//span//b//text()").extract()

        item["applyCount"] = div_list2[0] if div_list2 else None
        item["remind_count"] = div_list2[1] if div_list2 else None
        item["viewerCount"] = div_list2[2] if div_list2 else None

        deal_time_temp = response.xpath("//div[@class='d-article d-article2']//p[4]//text()").extract()
        # print(deal_time_temp)
        if deal_time_temp:
            deal_time = deal_time_temp[-1]
            # print(deal_time)
            item["deal_time"] = re.search(r"拍卖竞价确认时间：(.*?) ", deal_time).group(1) if deal_time else None

        #出价次数
        bid_count = response.xpath("//div[@class='tab-list']//span[@class='red']//text()").extract_first()
        item["bidCount"] = bid_count if bid_count else None


        #拍卖网址
        itemid = response.xpath("//input[@id='Web_Item_ID']//@value").extract_first()
        if itemid:
            item["item_id"] = itemid
            item["itemUrl"] = "http://www.gpai.net/sf/item2.do?Web_Item_ID={}".format(itemid)

        item["limit_status"] = "03"
        item["data_from"] = "s.gpai.net"

        detail_desc_temp = response.xpath('//div[@class="d-article d-article2"]//*//text()').extract()
        if detail_desc_temp:
            detail_desc_temp1 = ','.join(detail_desc_temp).strip()
            item["detail_desc"] = re.sub('\s', '', detail_desc_temp1).replace(',', '').replace('、', '')

        else:
            detail_desc_temp = response.xpath('//div[@class="richtext"]//*//text()').extract()
            if detail_desc_temp:
                detail_desc_temp1 = ','.join(detail_desc_temp).strip()
                item["detail_desc"] = re.sub('\s', '', detail_desc_temp1).replace(',', '').replace('、', '')


        print(item)
            # yield item






















