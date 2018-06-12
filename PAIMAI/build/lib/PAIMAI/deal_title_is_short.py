# -*- coding: utf-8 -*-
import datetime
import json
import re
from multiprocessing.pool import ThreadPool

import pymysql
from lxml import etree

import requests



def get_detail_desc():
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
        sql1 = "SELECT id,itemUrl from land_sum_info;"
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
            # bid_id = result["bid_id"]
            itemurl = result["itemUrl"]
            print(id, itemurl)
            """
            直接提取数据库中拍卖标的的itemurl，采用etree转化成element格式，获取ｊｓｏｎ数据链接地址
            """
            res = requests.get(itemurl)
            res = etree.HTML(res.text)
            detail_desc_temp = res.xpath("//div[@class='detail-common-text clearfix']/@data-from")[0]

            # print(type(record_url_temp))

            # print(response.text)
            # print(text.group(1))
            if text:
                res = etree.HTML(text.group(1))

                # item = response.meta['item']
                detail_desc_temp = res.xpath("//table//text()")[:]
                if len(detail_desc_temp) == 0:
                    detail_desc_temp = res.xpath("//p//text()")[:]
                detail_desc_a = ','.join(detail_desc_temp).strip()
                detail_desc = re.sub('\s', '', detail_desc_a).replace(',', '').replace('、','')
                # print(detail_desc)
                #
                # if detail_desc_temp is None:
                #     detail_desc_temp = res.xpath("//table//tr/td/text()")[:]
                # print(detail_desc_temp)
                # if detail_desc_temp is not None:
                #
                #     print(id,detail_desc)

                if detail_desc:
                    with conn.cursor() as cur2:
                        sql2 = "update new_auction_house set detail_desc = %s  where id = %s"
                        cur2.execute(sql2, (detail_desc,id))
                        conn.commit()
                        conn.cursor().close()
                        print("**" * 50)
                    print(id,detail_desc)


# 多线程，为了提高效率
# def multi():
#     pool = ThreadPool(processes=8)
#     pool.apply_async(get_detail_desc, ())
#     pool.close()
#     pool.join()

if __name__ == '__main__':
    starttime = datetime.datetime.now()
    # multi()
    get_detail_desc()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))