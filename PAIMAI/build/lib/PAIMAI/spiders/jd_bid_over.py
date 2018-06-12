# -*- coding: utf-8 -*-
import datetime
import json
import os
import re
from _md5 import md5
from json import JSONDecodeError

import time
from multiprocessing.pool import Pool
from urllib.parse import urlencode
from lxml import etree
import pymysql
import copy
import requests
from retrying import retry
# from config import *
class SiPaiSpider:
    def __init__(self):
        # self.table_name = table
        self.page_num = 10
        self.start_url = 'https://auction.jd.com/getJudicatureList.html?callback=jQuery5100855&page=1&childrenCateId=12728&paimaiStatus=2'
        #所有字段列表(23个)
        #self.main_fields = ['bid_id', 'title','bid_status', 'applyCount', 'viewerCount', 'bidCount','itemUrl','dealPrice',
                            # 'evaluatePrice','deal_time', 'deal_status','start_price','delay_count','court','contact',
                            # 'phone_num', 'limit_status','remind_count','img_url', 'coordinate','province', 'city', 'town','detailAdrress']

    # 解析链接,将html页面转化成文本形式
    @retry(stop_max_attempt_number=4)
    def parse_url(self,url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"

        }

        response = requests.get(url, headers=headers, timeout=5)
        assert response.status_code == 200
        json_data = response.text
        print(json_data)
        return json_data
        # try:
        #     html = json.loads(response)
        # # except UnicodeDecodeError:
        # except Exception:
        #     html = None
        # return html


    #将详情页面信息转化为element对象
    def get_page_detail(self,url):

        response = requests.get(url)
        if response.status_code == 200:
            try:
                html = response.content.decode('GBK')

            except Exception:
                html = response.text
            return etree.HTML(html)
        return None
    #
    # #解析列表页面json数据信息
    def parse_page_data(self,html):
        #使用正则匹配出ｊｓｏｎ数据
        # url_data = self.parse_url(html)
        # print(result)
        # if url_data:
        #     #将json数据转化成python字符串格式
        #     data = json.loads(url_data)
        #     print(data)
            #取出"data"的value信息
        json_content = requests.get(html).text
        # content = json_content[]

        print(type(json_content))
        # print(json_content)
        # content = json.loads(json_content)
        # print(type(content))
        # if content:
        # print(content)
            # data_list = content["ls"]
            # print(data_list)
            # return data_list

    # 在页面响应中找到url列表的页面,在请求的url中找到页数page_unm
    def get_page_index(self, page_num):
        #url_list = "https://auction.jd.com/getJudicatureList.html?callback=jQuery3087301&page=2&childrenCateId=12728"
        data = {
            'callback': 'jQuery4185843',
            'page': page_num,
            'childrenCateId': 12728,
            'paimaiStatus': 2

        }
        params = urlencode(data)
        base = 'https://auction.jd.com/getJudicatureList.html'
        url_start = base + '?' + params
        return url_start


    #获取json数据中详情页面的url链接，生成器itemUrl列表
    def get_detail_index(self,url):
        data_list = self.parse_page_data(url)
        for list in data_list:
            id = list.get("id")
            item_url = 'https://paimai.jd.com/' + id
            yield item_url

    # 主函数
    def main(self):
        # context = self.get_detail_index(start_url)
        # print(context)
        # 并获得详情页url列表
        detail_url_list = self.parse_url(self.start_url)
        print(detail_url_list)
        # pattern = re.compile(r'\((.*?)\)')
        # detail_url_pattern = re.search(pattern,detail_url_list)
        # print(detail_url_pattern.group(1))
        # 获取详情页信息
        # for detail_url in detail_url_list:
        #     # detail_urls = "https:" + detail_url
        #     print(detail_url)
    # 解析文本信息，获取详情页面的信息
    # def parse_page_detail(self,page):
    #     if page is not None:
    #         self.item = {}
    #         #拍卖id
    #         self.item["bid_id"] = page.xpath("//input[@id='J_ItemId']/@value")[0]
    #
    #         #拍卖网址
    #         self.item["itemUrl"] = "https://sf.taobao.com/sf_item/" + self.item["bid_id"] + ".htm"
    #         # print(self.item["itemUrl"])
    #         #标的物名称title
    #         title = page.xpath("//div[@class='grid-c']//h1/text()")[0].strip()
    #         # print(title)
    #         #拍卖次数与标的物名称分离
    #         title_status = title.split("【")[-1].split("】")[0]
    #         if title_status == '第一次拍卖':
    #             self.item["bid_status"] = '01'
    #         elif title_status == '第二次拍卖':
    #             self.item["bid_status"] = '02'
    #         elif title_status == '第三次拍卖':
    #             self.item["bid_status"] = '03'
    #         elif (title_status == '重新拍卖') or (title_status == '再次拍卖'):
    #             self.item["bid_status"] = '04'
    #         elif title_status == '变卖':
    #             self.item["bid_status"] = '05'
    #         # print(self.item["bid_status"])
    #
    #         item_title = title.split("【")[-1].split("】")[-1]
    #         #去掉＇（破）＇关键字
    #         if item_title.startswith("（"):
    #             self.item["title"] = item_title.split("）")[1]
    #         else:
    #             self.item["title"] = item_title
    #         # print(self.item["title"])
    #
    #         div_list1 = page.xpath("//div[@class='pm-main-l auction-interaction']")
    #         for div in div_list1:
    #             #成交时间
    #             # self.item["deal_time"] = div.xpath(".//span[2]/text()")[0]
    #             deal_time =  div.xpath(".//span[@class='countdown J_TimeLeft']/text()")
    #             if len(deal_time)>0:
    #                 self.item["deal_time"] = div.xpath(".//span[@class='countdown J_TimeLeft']/text()")[0]
    #             else:
    #                 self.item["deal_time"] = None
    #             #交易状态
    #             # print(self.item["deal_time"])
    #             status_text = div.xpath(".//li[@id='sf-price']/span/text()")
    #             if len(status_text)>0:
    #                 status_str = status_text[0]
    #                 if status_str == "成交价":
    #                     self.item["deal_status"] = "01"
    #                 else:
    #                     self.item["deal_status"] = "02"
    #             else:
    #                 self.item["deal_status"] = "01"
    #             #成交价格
    #             deal_price = div.xpath(".//span[@class='pm-current-price J_Price']/em/text()")[:]
    #             # print(deal_price)
    #             if len(deal_price)>0:
    #                 self.item["dealPrice"] = div.xpath(".//span[@class='pm-current-price J_Price']/em/text()")[0]
    #             else:
    #                 self.item["dealPrice"] = None
    #             #起拍价格
    #             start_price = div.xpath(".//span[3]/em/text()")[:]
    #             if len(start_price) > 0:
    #                 self.item["start_price"] = div.xpath(".//span[@class='J_Price']/text()")[0]
    #             else:
    #                 self.item["start_price"] = None
    #
    #             #延迟次数
    #             deal_time = div.xpath(".//span[3]/em/text()")[:]
    #             if len(deal_time)>0:
    #                 self.item["delay_count"] =div.xpath(".//span[3]/em/text()")[0]
    #             else:
    #                 self.item["delay_count"] = None
    #             #法院
    #             court = div.xpath(".//div[@class='pai-info']/p[2]/a/text()")[:]
    #
    #             if len(court)>0:
    #                 self.item["court"] = div.xpath(".//div[@class='pai-info']/p[2]/a/text()")[0]
    #             else:
    #                 self.item["court"] = ''
    #             #联系人
    #             contact = div.xpath(".//div[@class='pai-info']/p[3]/em/text()")[0]
    #             if len(contact)>0:
    #                 self.item["contact"] = div.xpath(".//div[@class='pai-info']/p[3]/em/text()")[0]
    #             else:
    #                 self.item["contact"] = None
    #             #联系电话
    #             tell_phone =  div.xpath(".//div[@class='pai-info']/p[3]/text()")[-1].strip().strip('/')
    #             if len(tell_phone)>0:
    #                 self.item["phone_num"] = div.xpath(".//div[@class='pai-info']/p[3]/text()")[-1].strip().strip('/')
    #             else:
    #                 self.item["phone_num"] = None
    #         #判断是否限购
    #         limit_status = page.xpath("//div[@class='module-sf']//h1/span[2]/i/text()")
    #         if len(limit_status)>0:
    #             self.item["limit_status"] = "02"
    #         else:
    #             self.item["limit_status"] = "01"
    #
    #         div_list2 = page.xpath("//div[@class='pm-main clearfix']")
    #         for div in div_list2:
    #             # 提醒人数
    #             remind_count = div.xpath(".//span[@class='pm-reminder i-b']/em/text()")[0]
    #             if len(remind_count)>0:
    #                 self.item["remind_count"] = div.xpath(".//span[@class='pm-reminder i-b']/em/text()")[0]
    #             else:
    #                 self.item["remind_count"] = None
    #             #报名人数
    #             applycount = div.xpath(".//span[@class='pm-apply i-b']/em/text()")
    #             if len(applycount)>0:
    #                 self.item["applyCount"] = applycount[0]
    #             else:
    #                 self.item["applyCount"] = None
    #             # print(self.item["applyCount"])
    #             #围观人数
    #             viewcount =  div.xpath(".//span[@class='pm-surround i-b']/em/text()")
    #             if len(viewcount)>0:
    #                 self.item["viewerCount"] = viewcount[0]
    #             else:
    #                 self.item["viewerCount"] = None
    #             # print(self.item["viewerCount"])
    #             #评估价格
    #             evaluatprice =  div.xpath(".//span[@class='J_Price']/text()")
    #             if len(evaluatprice)>0:
    #                 self.item["evaluatePrice"] = evaluatprice[0]
    #             else:
    #                 self.item["evaluatePrice"] = None
    #         #图片地址
    #         url_list = page.xpath("//div[@class='pm-main-l']//img/@src")[:]
    #         if url_list:
    #             for url in url_list:
    #                 self.item["img_url"] = "https:" + url.split("_80x80")[0]
    #
    #         #位置坐标
    #             self.item["coordinate"] = page.xpath("//input[@type='hidden'][last()]/@value")[-1]
    #         Location = page.xpath("//div[@class='detail-common-text']/text()")[:][-1].strip()
    #         # print(Location)
    #         if Location:
    #             self.item["province"] = Location.split(" ")[0][-2:]
    #             self.item["city"] = Location.split(" ")[1] if len(Location.split(" "))>=2 else None
    #             self.item["town"] = Location.split(" ")[2] if len(Location.split(" "))>=3 else None
    #             self.item["detailAdrress"] = Location.split(" ")[3][:] if len(Location.split(" "))>3 else None
    #
    #         #出价次数
    #         bid_count = page.xpath("//div[@class='module-sf']//span[@class='J_Record']/text()")
    #         # print(bid_count)
    #         if len(bid_count)>0:
    #             self.item["bidCount"] = bid_count[0].strip()
    #         # print(self.item["bidCount"])
    #
    #         #标的物详情描述,正则匹配（异步加载）
    #         detail = page.xpath("//div[@class='detail-common-text clearfix']/@data-from")[0]
    #         #获取json数据链接
    #         detail_url = 'https:' + detail
    #         detail_page = self.get_page_detail(detail_url)
    #         # print(detail_page)
    #         detail_desc = detail_page.xpath("//span/text()")
    #         if len(detail_desc) > 0:
    #             self.item["detail_desc"] = ','.join(detail_desc).strip()
    #         else:
    #             self.item["detail_desc"] = None
    #
    #         # print(self.item["detail_desc"])
    #         print(self.item)
    #         return self.item

    #保存数据到txt文档中
    # def save_content_list(self,content_list):
    #     with open("content.txt", "a") as f:
    #         for content in content_list:
    #             json.dump(content, f, ensure_ascii=False, indent=2)
    #             f.write("\n")

    #插入数据库
    # def insertdb(self,table_name,main_fields,item):
    #     self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="mysql", db="sipai", charset="utf8")
    #     self.cur = self.conn.cursor()
    #     #执行sql语句采用下面这种方式可以简化代码，main_fields 为所有字段列表，item为所有信息的字典
    #     sql = 'INSERT INTO {0}({1}) VALUES({2})'.format(table_name,','.join(main_fields),','.join(['%s'] * len(main_fields)))
    #     args = [item[k] for k in main_fields]
    #     arg = tuple(args)
    #     print(arg)
    #     try:
    #         self.cur.execute(sql,arg)
    #         self.conn.commit()
    #         print("提交成功")
    #     except:
    #         self.conn.rollback()
    #     finally:
    #         self.cur.close()
    #         self.conn.close()
        # 传统的sql执行语句
        # sql = "INSERT INTO informa(bid_id, title, applyCount,viewerCount,bidCount, itemUrl, dealPrice,evaluatePrice) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"
        # self.cur.execute(sql,(item["bid_id"],item["title"],item["applyCount"],item["viewerCount"],item["bidCount"],item["itemUrl"],item["dealPrice"],item["evaluatePrice"]))
        # self.cur.execute(sql%('1','2','3','4','5','6','7','8'))


            # detail_pages = self.get_page_detail(detail_urls)
            # print(detail_pages)
            # item = self.parse_page_detail(detail_pages)
            # print(item)

    # 开启进程池
    # def multi(self):
    #     pool = Pool(processes=8)
    #     groups = ([i for i in range(1, page_num)])
    #     pool.map(self.main, groups)
    #     pool.close()
    #     pool.join()


if __name__ == '__main__':
    sipai = SiPaiSpider()
    # starttime = datetime.datetime.now()
    # sipai.multi(
    sipai.main()
    # endtime = datetime.datetime.now()
    # time = (endtime - starttime).seconds
    # print("共耗时%s秒" % (time) )

