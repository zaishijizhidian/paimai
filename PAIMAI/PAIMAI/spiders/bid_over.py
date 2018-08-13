# -*- coding: utf-8 -*-
import json
import logging
import re
import time
import uuid
from copy import deepcopy
from datetime import date, timedelta

import requests
import scrapy
from PAIMAI.items import PaimaiItem
from lxml import etree

from model.coordinate  import get_latlng
from model.deal_taobao_aution_info import parse_table, get_rep_url
from model.deal_detail_desc_is_short import get_detail_desc
from model.deal_house_area import get_house_area
from model.deal_house_property_cardnum import get_house_cardnum
from model.modify_house_type import modify_type

logger = logging.getLogger("land_info")

class SipaiSpider(scrapy.Spider):
    name = "bid_over"
    # redis_key = 'SipaiSpider:start_urls'
    allowed_domains = ['sf.taobao.com']
    #所有类别的起始网址(更新日期2018-05-16至2018-06-22)

    # today = date.today()
    today = '2018-07-20'
    # yes = today - timedelta(days=1)
    yes = '2018-07-19'
    start_url = 'https://sf.taobao.com/item_list.htm?spm=a213w.7398504.filter.46.rDN4gv&sorder=-1&auction_start_seg=0&auction_start_from={}&auction_start_to={}'.format(yes,today)
    start_urls = [start_url]

    def parse(self, response):
        #添加日志信息
        #logger.info('info on %s', response.url)
        #logger.warning('WARNING on %s', response.url)
        #logger.debug('info on %s', response.url)
        #logger.error('info on %s', response.url)

        #获取某一省所有市的url链接
        # print(1111)
        # div_list = response.xpath("//div[@class='sub-condition J_SubCondition']//ul")
        provice_list = response.xpath('//div[@class="sf-filter-value"]/ul/li[@class="triggle"]')
        # 遍历所有省,找出所有市的url
        for provice in provice_list:
            item = {}
            # print(111)
            provice_url = provice.xpath("./em/a/@href").extract_first()
            if provice_url:
                item["province_url"] = "https:" + provice_url.strip()
                yield scrapy.Request(
                    item["province_url"], callback=self.get_city_url, dont_filter=True
                )

    def get_city_url(self,response):
        city_list = response.xpath('//div[contains(@class,"sub-condition")]//ul/li')
        #遍历所有市,找出所有县的url
        for city in city_list:
            item = {}
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
        item = PaimaiItem()
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

                #在列表页获取部分json 信息
                for list in data_list:
                    detail_url = list.get("itemUrl")
                    item["itemUrl"] ="https:" +  detail_url
                    # item["item_id"] = str(list.get("id"))
                    item["dealPrice"] = str(list.get("currentPrice")*1000)#成交价格,单位为厘
                    # print(item["dealPrice"])
                    item["evaluatePrice"] = str(list.get("consultPrice")*1000)#评估价，单位为厘
                    item["viewerCount"] = str(list.get("viewerCount"))
                    item["bidCount"] = str(list.get("bidCount"))
                    item["delay_count"] = str(list.get("delayCount"))
                    item["applyCount"] = str(list.get("applyCount"))
                    start_time = list.get("start")
                    end_time = list.get("end")
                    start_timeArray = time.localtime(start_time / 1000)
                    end_timeArray = time.localtime(end_time / 1000)
                    status = list.get("status")
                    if status == 'doing':
                        item["deal_status"] = '05'
                        item["deal_time"] = time.strftime("%Y-%m-%d %H:%M:%S", start_timeArray) #正在进行的，交易时间取开始时间
                    elif status == 'todo':
                        item["deal_status"] = '00'
                        item["deal_time"] = time.strftime("%Y-%m-%d %H:%M:%S", start_timeArray) #即将开始的，交易时间取开始时间
                    elif status == 'done':
                        item["deal_status"] = '01'
                        item["deal_time"] = time.strftime("%Y-%m-%d %H:%M:%S", end_timeArray) #成交的取结束时间
                    elif status == 'failure':
                        item["deal_status"] = '02'
                        item["deal_time"] = time.strftime("%Y-%m-%d %H:%M:%S", end_timeArray) #流拍的取结束时间
                    elif status == 'break':
                        item["deal_status"] = '04'
                        item["deal_time"] = time.strftime("%Y-%m-%d %H:%M:%S", end_timeArray) #中止的取结束时间
                    elif status == 'revocation':
                        item["deal_status"] = '03'
                        item["deal_time"] = time.strftime("%Y-%m-%d %H:%M:%S", end_timeArray) #撤回的取结束时间

                    item["title"] = list.get("title")

                    # 生成唯一标识的uuid信息
                    u = uuid.uuid5(uuid.NAMESPACE_OID, item["title"])
                    # 生成12位的整数数字唯一标识
                    item["bid_id"] = u.time_low

                    yield scrapy.Request(
                        item["itemUrl"],callback=self.parse_detail_url,meta={"item":deepcopy(item)}
                    )
        # 获取下一页的url列表
        next_page_url = response.xpath("//div[@class='pagination J_Pagination']/a[@class='next']/@href").extract_first()
        #page_num = response.xpath("//div[@class='pagination J_Pagination']//em[@class='page-total']/text()").extract_first()
        if next_page_url is not None:
            next_url = "https:" + next_page_url.strip()
            yield scrapy.Request(
                next_url,
                callback=self.get_detail_url
            )

    def parse_detail_url(self, response):
        item = response.meta["item"]
        # 拍卖id
        item["item_id"] = response.xpath("//input[@id='J_ItemId']/@value").extract_first()

        # 拍卖网址
        # item["itemUrl"] = "https://sf.taobao.com/sf_item/" + item["bid_id"] + ".htm"
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
        else:
            item["bid_status"] = None

        # 起拍价格
        start_price = response.xpath("//div[@class='pm-main-l auction-interaction']//span[@class='J_Price']/text()").extract_first()
        # print(start_price)
        if start_price:
            item["start_price"] = str(float(start_price.replace(',', ''))*1000) #1,120,000
        else:
            item["start_price"] = None

        # # 延迟次数

        div_list = response.xpath("//div[@class='subscribe']//span[@class='unit-txt']")
        # 法院
        court = div_list.xpath(".//a/text()").extract_first()
        item["court"] = court if court is not None else None

        # print(court)
        # print("===" * 20)
        # 联系人
        contact = div_list.xpath(".//em/text()").extract_first()
        item["contact"] = contact if contact is not None else None

        # 联系电话
        tell_phone = div_list.xpath("./text()").extract()
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

        # 图片地址
        urllist = []
        url_list = response.xpath("//div[@class='pm-main-l']//img/@src").extract()

        if url_list:
            for url in url_list:
                img_url = "https:" + url.split("_80x80")[0]
                urllist.append(img_url)
            item["img_url"] = str(urllist)

        #数据来源平台
        item["data_from"] = "sf.taobao.com"
        item["create_time"] = date.today()
        item["edit_time"] = date.today()

        # 位置坐标,如果能提取到经纬度坐标，直接切分为经度和纬度，如果提取不到，调用百度api通过标的title获取到经纬度get_latlng()模块
        coordinate = response.xpath("//input[@type='hidden'][last()]/@value").extract()
        if coordinate:
            coordinate_temp= coordinate[-1]
            try:
                item["longtitude"] = coordinate_temp.split(',')[0]
                item["latitude"] = coordinate_temp.split(',')[1]
            except Exception as e:
                print(e,"error url is",item["itemUrl"])
                item["coordinate"] = '0'
                item["latitude"] = '0'
                item["longtitude"] = '0'
                item["confidence"] = None
            item["coordinate"] = item["latitude"] + ',' + item["longtitude"]
            item["confidence"] = None


        else:
            confidence, lat, lng = get_latlng(item["title"])
            item["confidence"] = confidence
            item["longtitude"] = lng
            item["latitude"] = lat
            item["coordinate"] = str(lat) + ',' + str(lng)

        # print(item["coordinate"])
        Location = response.xpath("//div[@class='detail-common-text']//div[@id='itemAddress']/text()").extract_first()
        if Location:
            ls = Location.split(" ")
            item["province"] = ls[0]
            item["city"] = ls[1]
            item["town"] = ls[2] if len(ls) >= 3 else None
            item["detailAdrress"] = response.xpath("//div[@class='detail-common-text']//div[@id='itemAddressDetail']/text()").extract_first().strip()


        # 标的物详情描述,正则匹配（异步加载）
        detail = response.xpath("//div[@class='detail-common-text clearfix']/@data-from").extract_first()
        # 获取json数据链接
        detail_url =  'https:' + detail

        data_item = parse_table(detail_url)
        try:
            item["auction_people"] = data_item["auction_people"]
        except Exception:
            item["auction_people"] = ''
        try:
            item["jdu_doc_number"] = data_item["jdu_doc_number"]
        except Exception :
            item["jdu_doc_number"] = ''
        try:
            item["legal_remark"] = data_item["legal_remark"]
        except Exception :
            item["legal_remark"] = ''
        try:
            item["house_useage_detail"] = data_item["house_useage_detail"]
        except Exception:
            item["house_useage_detail"] = ''
        data_url = 'https://sf.taobao.com/json/get_gov_attach.htm?id=' + item['item_id']
        item['report_url'] = get_rep_url(data_url)
        if item["house_useage_detail"]:
            if '商业' in item["house_useage_detail"] or '商服' in item["house_useage_detail"]:
                item['house_type'] = '03'
            elif '工业' in item["house_useage_detail"]:
                item['house_type'] = '06'
            elif '住宅' in item["house_useage_detail"]:
                item['house_type'] = '01'
            elif '办公' in item["house_useage_detail"]:
                item['house_type'] = '02'
            elif '车库' in item["house_useage_detail"] or '停车场'in item["house_useage_detail"]:
                item['house_type'] = '04'
            else:
                item['house_type'] = modify_type(item["title"])
        else:
            item['house_type'] = modify_type(item["title"])


        res = requests.get(detail_url)
        res = etree.HTML(res.text)

        # item = response.meta['item']
        detail_desc = res.xpath("//*/text()")

        # print(detail_desc)

        if detail_desc is not None:
            detail_desc_temp = ','.join(detail_desc).strip()
            item["detail_desc"] = re.sub('\s', '', detail_desc_temp).replace(',', '').replace('、', '')
            if len(item["detail_desc"]) < 50:
                # 变卖公告
                detail_desc_temp_url = res.xpath("//div[@id='J_NoticeDetail']/@data-from")
                # print(type(record_url_temp))
                if detail_desc_temp_url:
                    detail_desc_url = 'https:' + detail_desc_temp_url[0]
                    item["detail_desc"] = get_detail_desc(detail_desc_url)
                        # print(item["detail_desc"])

        item['house_card_num'] = get_house_cardnum(item["detail_desc"])
        item['total_house_area'],item['total_land_area'] = get_house_area(item["detail_desc"])
        print("=====" * 20)
        yield item







