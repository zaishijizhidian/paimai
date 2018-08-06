# -*- coding: utf-8 -*-
import logging
import time
import uuid
from copy import deepcopy
from datetime import date

import scrapy

from get_data_id import *
from jd_sipai.module.coordinate import get_latlng
from jd_sipai.module.deal_house_area import get_house_area
from jd_sipai.module.deal_house_property_cardnum import get_house_cardnum
from jd_sipai.module.deal_jd_aution_info import parse_table, get_rep_url
from model.modify_house_type import modify_type

logger = logging.getLogger("jd_info")

from jd_sipai.items import JdSipaiItem
class JdBidSpider(scrapy.Spider):
# class JdBidSpider(RedisSpider):
    name = 'jd_bid_over'
    allowed_domains = ['jd.com','auction.jd.com']
    start_urls = iter(get_item_url())
    # def __int__(self):
    #     # redis_key = 'JdBidSpider:start_urls'
    #     # start_urls = ['https://auction.jd.com/getJudicatureList.html?callback=jQuery5223987&page=1&limit=40&_=1526613080129']
    #     for item_url in start_urls:
    #         yield scrapy.Request(
    #             item_url,
    #             callback=self.parse_item
    #         )
    def parse(self, response):
        # 添加日志信息
        logger.info('info on %s', response.url)
        logger.warning('WARNING on %s', response.url)
        logger.debug('info on %s', response.url)
        logger.error('info on %s', response.url)
        item = JdSipaiItem()
        pattern = re.search(r'"ls":(.*?),"total"',response.body.decode())
        json_content = json.loads(pattern.group(1))
        pattern_list = list(json_content)
        for content in pattern_list:
            item["item_id"] = str(content["id"])
            # print("*****",item["item_id"])
            item["itemUrl"] = "https://paimai.jd.com/" + item["item_id"]
            item["dealPrice"] = str(content["currentPrice"]*1000)
            item["evaluatePrice"] = str(content["assessmentPrice"]*1000)
            start_time = content["startTime"]
            end_time = content["endTime"]
            startimeArray = time.localtime(start_time/1000)  # 将毫秒转化为当前时间格式
            endtimeArray = time.localtime(end_time/1000)  # 将毫秒转化为当前时间格式
            item["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S", startimeArray)
            item["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S", endtimeArray)
            item["title"] = content["title"]
            if item["title"]:
                confidence, lat, lng = get_latlng(item["title"])
                item["confidence"] = confidence
                item["longtitude"] = lng
                item["latitude"] = lat
                if lng:
                    item["coordinate"] = lng + ',' + lat
                else:
                    item["coordinate"] = ''
                # 生成唯一标识的uuid信息
                u = uuid.uuid5(uuid.NAMESPACE_OID, item["title"])
                # 生成12位的整数数字
                item["bid_id"] = str(u.time_low)
            yield scrapy.Request(
                item["itemUrl"],
                callback=self.parse_detail_url,
                meta={"item":deepcopy(item)}
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

        item["data_from"] = 'https://auction.jd.com'
        item["create_time"] = date.today()
        item["edit_time"] = date.today()

        # div_list2 = response.xpath('//div[@class="pm-support"]//input[@id="consultName"]//@value')
        item["contact"] = response.xpath('//div[@class="pm-support"]//input[@id="consultName"]//@value').extract_first()
        item["phone_num"] = response.xpath('//div[@class="pm-support"]//input[@id="consultTel"]//@value').extract_first()
        # item["deal_time"] = response.xpath('//div[@class="pm-support"]//input[@id="endTime"]//@value').extract_first()

        start_price = response.xpath("//div[@class='pm-attachment']//ul/li[@class='fore1'][2]//em/text()").extract_first()
        if start_price:
            price = start_price.split('¥')[1].strip().replace(',', '')

            item["start_price"] = str(float(price)*1000)
        else:
            item["start_price"] = None
        # evaluateprice = response.xpath("//div[@class='pm-attachment']//ul/li[@class='fore3']//em/text()").extract_first()
        # item["evaluatePrice"] = evaluateprice.split('¥')[1] if evaluateprice else None
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

            if "bidCount" in text1_dict.keys():
                item["bidCount"] = str(text1_dict["bidCount"])
                item["delay_count"] = text1_dict["delayedCount"]
                item["remind_count"] = '0'
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
                    item["deal_time"] = item["start_time"] #预告取开始时间
                elif auctionStatus == '1':
                    item["deal_status"] = '05'
                    item["deal_time"] = item["start_time"] #正在进行取开始时间
                elif auctionStatus == '2':
                    if displayStatus == '1':
                        item["deal_status"] = '01'
                        item["deal_time"] = item["end_time"] #成交取结束时间
                    if displayStatus == '6':
                        item["deal_status"] = '02'
                        item["deal_time"] = item["end_time"]  # 暂缓取结束时间
                    if displayStatus == '5':
                        item["deal_status"] = '03'
                        item["deal_time"] = item["end_time"]  # 撤销取结束时间
                    if displayStatus == '7':
                        item["deal_status"] = '04'
                        item["deal_time"] = item["end_time"]  # 终止取结束时间


            else:
                item["bidCount"] = '0'

            item["view_url"] = "https://paimai.jd.com/json/ensure/queryAccess?&paimaiId={}".format(item["item_id"])
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
                item["applyCount"] = str(text1_dict["accessEnsureNum"])
                item["viewerCount"] = str(text1_dict["accessNum"])
            else:
                item["applyCount"] = '0'
                item["viewerCount"] = '0'

        item["paimai_detail_url"] = 'https://paimai.jd.com/json/paimaiProduct/productDesciption?productId={}'.format(
            item["skuId"])

        data_item = parse_table(item["paimai_detail_url"])
        try:
            item["auction_people"] = data_item["auction_people"]
        except Exception:
            item["auction_people"] = ''
        try:
            item["jdu_doc_number"] = data_item["jdu_doc_number"]
        except Exception:
            item["jdu_doc_number"] = ''
        try:
            item["legal_remark"] = data_item["legal_remark"]
        except Exception:
            item["legal_remark"] = ''
        try:
            item["house_useage_detail"] = data_item["house_useage_detail"]
        except Exception:
            item["house_useage_detail"] = ''


        data_url = 'https://paimai.jd.com/json/paimaiProduct/queryProductFiles?productId='.format(['item_id'])
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
            elif '车库' in item["house_useage_detail"] or '停车场' in item["house_useage_detail"]:
                item['house_type'] = '04'
            else:
                item['house_type'] = modify_type(item["title"])
        else:
            item['house_type'] = modify_type(item["title"])


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
            item['house_card_num'] = get_house_cardnum(item["detail_desc"])
            item['total_house_area'], item['total_land_area'] = get_house_area(item["detail_desc"])

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





























