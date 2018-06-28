# -*- coding: utf-8 -*-
import datetime
import json
import re
from multiprocessing.pool import ThreadPool

import pymysql
from lxml import etree

import requests

def get_detail_desc():
    conn = pymysql.connect(#host='www.npacn.com',
                           host='192.168.11.251',
                           port=3306,
                           user='root',
                           # user='zxlh',
                           password='youtong123',
                           # password='8dMPjf1jIW8c',
                           # database='sipa_customer',
                           database='sipai',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构


    with conn.cursor() as cur1:
        """首先建一张new_bid_id的表，这里的bid_id与new_bid_record中的bid_id关联，形成一对多的联系"""
        # sql1 = "SELECT id,itemUrl from `last_status(03)` where detail_desc = '';"
        sql1 = "SELECT id,itemUrl from `01_new_auction_info` where LENGTH (detail_desc)< 30 and id >363121;"
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
            # print(id, itemurl)
            """
            直接提取数据库中拍卖标的的itemurl，采用etree转化成element格式，获取ｊｓｏｎ数据链接地址
            """
            res = requests.get(itemurl)
            res = etree.HTML(res.text)
            #标的物介绍
            detail_desc_temp_url = res.xpath("//div[@class='detail-common-text clearfix']/@data-from")[0]
            #变卖公告
            # detail_desc_temp_url = res.xpath("//div[@id='J_NoticeDetail']/@data-from")[0]
            # print(type(record_url_temp))
            detail_desc_url = 'https:' + detail_desc_temp_url

            #获取json文本，转化成element对象
            response = requests.get(detail_desc_url)

            res = etree.HTML(response.text)
            detail_desc = res.xpath("//*//text()")

            # print(detail_desc)
            print("=====" * 20)
            item = {}
            if detail_desc :
                detail_desc_temp = ','.join(detail_desc).strip()
                item["detail_desc"] = re.sub('\s', '', detail_desc_temp).replace(',', '').replace('\\','')
            else:

                item["detail_desc"] = re.sub('<br\s*?/?>','',response.text)



            print(item["detail_desc"])
            # with conn.cursor() as cur2:
            #     sql2 = "update `last_status(03)` set detail_desc = %s  where id = %s"
            #     cur2.execute(sql2, (item["detail_desc"], id))
            #     conn.commit()
            #     conn.cursor().close()
            # print("**" * 50)



            #获取标的物介绍的文本
            # detail_desc_temp = res.xpath("//table//text()") or res.xpath("//p//text()")
            #获取变卖公告的文本
            """
            detail_desc_temp = res.xpath("//span//text()")
            if detail_desc_temp:
                detail_desc_1 = ','.join(detail_desc_temp).strip()
                ds = re.sub('\s', '', detail_desc_1).replace(',', '').replace('、', '')
                # print(id,detail_desc)
                detail_desc_text2 = re.search(r"标的(.*?)二", ds)
                if detail_desc_text2:
                    detail_desc_text = re.search(r"性质.*", detail_desc_text2.group(0))
                    if detail_desc_text:
                        detail_desc_2 = detail_desc_text.group(0)
                    else:
                        detail_desc_2 = None
                    if detail_desc_2:
                        print(id, itemurl, detail_desc_2)
                        with conn.cursor() as cur2:
                            sql2 = "update 01_new_auction_info set house_useage_detail = %s  where id = %s"
                            cur2.execute(sql2, (detail_desc_2,id))
                            conn.commit()
                            conn.cursor().close()
                        print("**" * 50)
            """


# 多线程，为了提高效率
def multi():
    pool = ThreadPool(processes=8)
    pool.apply_async(get_detail_desc, ())
    pool.close()
    pool.join()

if __name__ == '__main__':
    starttime = datetime.datetime.now()
    multi()
    # get_detail_desc()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))