# -*- coding: utf-8 -*-
import json
import re
from lxml import etree

import requests
import scrapy
from copy import deepcopy
from PAIMAI.items import PaimaiItem

# import logging
# logger = logging.getLogger(__name__)


class SipaiSpider(scrapy.Spider):
    # name = 'sipai'
    allowed_domains = ['sf.taobao.com']
    # start_urls = ['https://sf.taobao.com/item_list.htm?spm=a213w.7398504.filter.13.7XgpPV&category=50025969&city=&province=&sorder=2&auction_start_seg=-1']
    start_urls = ['https://sf.taobao.com/item_list.htm?spm=a213w.7398504.filter.14.vyOF5H&category=50025969&city=&province=%D5%E3%BD%AD&sorder=2&auction_start_seg=-1']

    def parse(self, response):
        #获取某一省所有市的url链接
        # print(1111)
        # div_list = response.xpath("//div[@class='sub-condition J_SubCondition']//ul")
        div_list = response.xpath('//div[contains(@class,"sub-condition")]//ul/li')
        #遍历所有市,找出所有县的url
        for city in div_list:
            item = {}
            # print(111)
            city_url = city.xpath("./em/a/@href").extract_first()
            if city_url:
                item["city_url"] = "https:" + city_url.strip()
                yield scrapy.Request(
                item["city_url"], callback=self.get_town_url,dont_filter=True
                )
            # print(item["city_url"])
            # logging.info(item["city_url"])


    def get_town_url(self,response):
        #获取所有县的url链接
        town_list = response.xpath("//div[contains(@class,'sub-condition J_SubCondition ')]//ul/li")
        # print("*"*20,town_list)
        for town in town_list:
            item={}
            town_url = town.xpath("./em/a/@href").extract_first()
            if town_url is not None:
                item["town_url"] = "https:" + town_url.strip()
                yield scrapy.Request(
                    item["town_url"], callback = self.get_detail_url,dont_filter=True
                )
            # print(item["town_url"])


    def get_detail_url(self,response):
        # 使用正则匹配出ｊｓｏｎ数据
        data_pattern = re.compile('<script id="sf-item-list-data" type="text/json">(.*?)</script>', re.S)
        result = re.search(data_pattern, response.body.decode('GBK'))
        if result:

            #将json数据转化成python字符串格式
            data = json.loads(result.group(1))
            #取出"data"的value信息
            if data and 'data' in data.keys():
                data_list = data.get('data')
                # print(data_list)

                for list in data_list:
                    item = {}
                    detail_url = list.get("itemUrl")
                    item['detail_url'] ="https:" +  detail_url
                    yield scrapy.Request(
                        item['detail_url'],callback=self.parse_detail_url
                    )

        # 获取下一页的url列表
        next_page_url = response.xpath("//div[@class='pagination J_Pagination']/a[@class='next']/@href").extract_first()
        # page_num = response.xpath("//div[@class='pagination J_Pagination']//em[@class='page-total']/text()").extract_first()
        if next_page_url is not  None:
            next_url = "https:" + next_page_url.strip()
            yield scrapy.Request(
                next_url,
                callback=self.get_detail_url
            )


    def parse_detail_url(self, response):
            item = PaimaiItem()
            # 拍卖id
            item["bid_id"] = response.xpath("//input[@id='J_ItemId']/@value").extract_first()

            # 拍卖网址
            item["itemUrl"] = "https://sf.taobao.com/sf_item/" + item["bid_id"] + ".htm"
            # print(self.item["itemUrl"])
            # 标的物名称title
            title = response.xpath("//div[@class='grid-c']//h1/text()").extract_first().strip()

            # print(title)
            # 拍卖次数与标的物名称分离
            title_status = title.split("【")[-1].split("】")[0]
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
            # print(self.item["bid_status"])

            item_title = title.split("【")[-1].split("】")[-1]
            # 去掉＇（破）＇关键字
            if item_title.startswith("（"):
                item["title"] = item_title.split("）")[1]
            else:
                item["title"] = item_title
            # print(self.item["title"])
            div_list1 = response.xpath("//div[@class='pm-main-l auction-interaction']//ul/li")

            # 成交时间
            # self.item["deal_time"] = div.xpath(".//span[2]/text()")[0]
            item["deal_time"]= div_list1.xpath(".//span[@class='countdown J_TimeLeft']/text()").extract_first() if len(div_list1)>0 else None
            # print(item["deal_time"])


            # 交易状态
            # print(self.item["deal_time"])
            status_text = div_list1.xpath(".//span[@class='title']/text()").extract_first()
            # print(status_text)

            if len(status_text) > 0:
                if status_text == "成交价":
                    item["deal_status"] = "01"
                else:
                    item["deal_status"] = "02"
            else:
                item["deal_status"] = "01"
            # 成交价格
            deal_price = div_list1.xpath(".//span[@class='pm-current-price J_Price']/em/text()").extract_first()
            item["dealPrice"] = deal_price if deal_price is not None else None
            # print(deal_price)


            # 起拍价格
            start_price = response.xpath("//div[@class='pm-main-l auction-interaction']//span[@class='J_Price']/text()").extract_first()
            print(start_price)
            item["start_price"] = start_price if start_price is not None else None

            # 延迟次数
            deal_time = div_list1.xpath(".//span[3]/em/text()").extract_first()
            item["delay_count"] = deal_time if deal_time is not None else None
            div_list = response.xpath("//div[@class='pm-main-l auction-interaction']")
            # 法院
            court = div_list.xpath(".//div[@class='pai-info']/p[2]/a/text()").extract_first()
            item["court"] = court if court is not None else None

            # print(court)
            # print("===" * 20)
            # 联系人
            contact = div_list.xpath(".//div[@class='pai-info']/p[3]/em/text()").extract_first()
            item["contact"] = contact if contact is not None else None

            # 联系电话
            tell_phone = div_list.xpath(".//div[@class='pai-info']/p[3]/text()").extract()
            item["phone_num"] =tell_phone[-1].strip().strip('/') if tell_phone is not None else None
            # print(item["phone_num"])

            # 判断是否限购
            limit_status = response.xpath("//div[@class='module-sf']//h1/span[2]/i/text()").extract_first()

            item["limit_status"] = "02" if limit_status is not  None else "01"
            # print(item["limit_status"])
            # print('*' * 200)

            div_list2 = response.xpath("//div[@class='pm-main clearfix']")
            # for div in div_list2:
            # 提醒人数
            remind_count = div_list2.xpath(".//span[@class='pm-reminder i-b']/em/text()").extract_first()
            item["remind_count"] =remind_count if remind_count is not None else None
            # print(item["remind_count"])
            # print('*' * 200)
            # 报名人数
            applycount = div_list2.xpath(".//span[@class='pm-apply i-b']/em/text()").extract_first()
            item["applyCount"] = applycount if applycount is not None else None
            # print(item["applyCount"])
            # print('*' * 200)
            # print(self.item["applyCount"])
            # 围观人数
            viewcount = div_list2.xpath(".//span[@class='pm-surround i-b']/em/text()").extract_first()

            item["viewerCount"] = viewcount if viewcount is not None else None

            # print(item["viewerCount"])
            # print('*' * 200)
            # 评估价格
            evaluatprice = div_list2.xpath(".//span[@class='J_Price']/text()").extract_first()

            item["evaluatePrice"] = evaluatprice if evaluatprice is not None else None
            # print(item["evaluatePrice"])
            # print('*' * 200)
            # 图片地址
            url_list = response.xpath("//div[@class='pm-main-l']//img/@src").extract()
            if url_list:
                for url in url_list:
                    item["img_url"] = "https:" + url.split("_80x80")[0]
                    # print(item["img_url"])
                    # print('*' * 200)
            # 数据来源平台
            item["data_from"] = "sf.taobao.com"
            # 位置坐标
            coordinate = response.xpath("//input[@type='hidden'][last()]/@value").extract()
            item["coordinate"] = coordinate[-1] if coordinate is not None else None
            # print(item["coordinate"])
            Location = response.xpath("//div[@class='detail-common-text']/text()").extract()[-1].strip()
            if Location:
                item["province"] = Location.split(" ")[0][-2:]
                item["city"] = Location.split(" ")[1] if len(Location.split(" ")) >= 2 else None
                item["town"] = Location.split(" ")[2] if len(Location.split(" ")) >= 3 else None
                item["detailAdrress"] = Location.split(" ")[3][:] if len(Location.split(" ")) > 3 else None

            # 出价次数
            bid_count = response.xpath("//div[@class='module-sf']//span[@class='J_Record']/text()").extract_first()
            # print(bid_count)
            item["bidCount"] = bid_count.strip() if bid_count is not None else None

            # 标的物详情描述,正则匹配（异步加载）
            detail = response.xpath("//div[@class='detail-common-text clearfix']/@data-from").extract_first()
            # 获取json数据链接
            detail_url =  'https:' + detail
            # print(detail_url,"****"*20)
            # print(item)
            # yield scrapy.Request(
            #     detail_url,
            #     # callback=self.get_page_detail,priority=1,
            #     meta={'item': deepcopy(item)}
            # )
            res = requests.get(detail_url)
            res = etree.HTML(res.text)

            # item = response.meta['item']
            detail_desc = res.xpath("//span/text()")
            # print(detail_desc)
            print("=====" * 20)
            if detail_desc is not None:
                item["detail_desc"] = ','.join(detail_desc).strip()
            else:
                item["detail_desc"] = None

            # print(self.item["detail_desc"])
            #     print(item["detail_desc"])

            yield item




















