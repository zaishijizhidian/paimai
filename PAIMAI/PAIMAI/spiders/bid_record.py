# -*- coding: utf-8 -*-
import datetime
import json
import re
from multiprocessing.pool import ThreadPool

import pymysql
from lxml import etree

import requests



def get_bid_record():
    conn = pymysql.connect(#host='localhost',
                           host='192.168.11.251',
                           port=3306,
                           user='root',
                           password='youtong123',
                           # password='mysql',
                           # database='sipai_backup',
                           database='sipai',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构


    with conn.cursor() as cur1:
        """首先建一张new_bid_id的表，这里的bid_id与new_bid_record中的bid_id关联，形成一对多的联系"""
        sql1 = "SELECT id,bid_id,itemUrl from new_bid_id where id > 534608;"
        cur1.execute(sql1)
        #设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        #获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        for result in results:
            # print(111)
            #获取字典中的字段信息
            id = result["id"]
            bid_id = result["bid_id"]
            itemurl = result["itemUrl"]
            print(id, bid_id)
            """
            直接提取数据库中拍卖标的的itemurl，采用etree转化成element格式，获取ｊｓｏｎ数据链接地址
            """
            res = requests.get(itemurl,verify=False)
            res = etree.HTML(res.text)
            record_url_temp = res.xpath("//div[@class='introduce-bid J_Content']/@data-from")[0]

            # print(type(record_url_temp))
            record_url = 'https:' + record_url_temp
            # print(record_url)
            #获取json文本，转化成gbk格式
            response = requests.get(record_url, verify=False)
            result = response.content.decode('gbk')
            """
            在获取拍卖记录链接响应后，发现响应文本并不是正规的json数据格式，ｋｅｙ中并没有双引号，这给爬取工作带来一定难度，经过多天查找．发现可以采用正则替换json格式
            于是，将所有的key　都用双引号引起来，变成标准的json格式，s1,s2就是将数据类型匹配成标准json格式的过程
            """
            s1 = re.sub(r'([A-Za-z]\w+)', r'"\1"', result)
            s2 = re.sub(r'\""', '\"', s1)
            if s2:
                """转化成标准的json格式之后，再转化成python字符串形式，由于是python字典形式，可以采用字典的相关方法提取数据"""
                data = json.loads(s2)
                # print(type(data))
                totalcnt = data.get('totalCnt')
                if totalcnt != 0:
                    data_list = data.get('records')
                    # print(data_list)
                    for list in data_list:
                        bid_code = list.get('alias')
                        # print(bid_code)
                        bid_date = list.get('date')
                        bid_price = list.get('price')
                        bid_status = list.get('status')
                        # print(type(bid_status))
                        if bid_status == -1:
                            bid_status_code = '01'
                        else:
                            bid_status_code = '02'
                            """
                            在数据库中如何解决一个bid_id对应多个拍卖记录是出现了问题，要么是插入不进去，要么只能插入单条数据，花费了一天时间
                            解决这个问题：采用inset into语法，将对应的记录与另一张表中的bid_id 相关联，形成一对多的联系．在此之前要想建一张new_bid_id的表，然后插入时才可以形成关联
                            由于并不是每个标的都有拍卖记录，对于没有拍卖记录的标的选择忽略，只抓取由记录的标的
                            """
                        with conn.cursor() as cur2:
                            sql2 = "insert into 04_new_bid_record (bid_id,bid_code,bid_date,bid_price,bid_status_code)  VALUES (%s,%s,%s,%s,%s)"
                            cur2.execute(sql2, (bid_id,bid_code,bid_date,bid_price,bid_status_code))
                            conn.commit()
                            conn.cursor().close()
                            print("**" * 50)
                        print(bid_code,bid_date,bid_price,bid_status_code)
# 多线程，为了提高效率
def multi():
    pool = ThreadPool(processes=8)
    pool.apply_async(get_bid_record, ())
    pool.close()
    pool.join()

if __name__ == '__main__':
    starttime = datetime.datetime.now()
    multi()
    # get_bid_record()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))


    """
    最开始的思路是用scrapy框架获取所有的url然后爬取拍卖记录，后来发现数据库中已经有每个标的的itemUrl，所以采取直接在数据库中提取url的方式直接爬取拍卖记录,虽然已经淘汰
    但是这是一种解决问题的方式，如果没有之前的这一个过程，后面的思路就无从谈起了
    """

    # def parse_detail_url(self, response):
    #         item = PaimaiItem()
    #         # 拍卖id
    #         item["bid_id"] = response.xpath("//input[@id='J_ItemId']/@value").extract_first()
    #         # 出价次数
    #         # bid_count = response.xpath("//div[@class='module-sf']//span[@class='J_Record']/text()").extract_first()
    #         # print(bid_count)
    #         # item["bidCount"] = bid_count.strip() if bid_count is not None else None
    #         record_url= response.xpath("//div[@class='introduce-bid J_Content']/@data-from")
    #         item["record_url"] = "https:" +  record_url if record_url is not None else None
    #         yield scrapy.Request(
    #             item['record_url'], callback=self.parse_record_url,meta={"item":deepcopy(item)}
    #         )
    # def parse_record_url(self,response):
    #         item = response.meta["item"]
    #         result = response.body.decode('GBK')
    #         if result:
    #             # 将json数据转化成python字符串格式
    #             data = json.loads(result)
    #             # 取出"data"的value信息
    #             if data and 'records' in data.keys():
    #                 data_list = data.get('records')
    #                 # print(data_list)
    #                 for list in data_list:
    #                     item["bid_code"] = list.get('alias')
    #                     item["bid_date"]  = list.get('date')
    #                     item["bid_price"] = list.get('price')
    #                     bid_status = list.get('status')
    #                     if bid_status == '99':
    #                         item["bid_status"] = '02'
    #                     else:
    #                         item['bid_status'] = '01'
    #
    #
    #         # print(self.item["detail_desc"])
    #         #     print(item["detail_desc"])
    #
    #         yield item





















