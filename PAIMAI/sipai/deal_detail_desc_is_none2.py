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
        # sql1 = "SELECT id,itemUrl from 01_new_auction_info where LENGTH(detail_desc )< 20;"
        sql1 = "SELECT id,itemUrl from `001_house_sum_info` where LENGTH (detail_desc)< 50;"
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
            # detail_desc_temp_url = res.xpath("//div[@class='detail-common-text clearfix']/@data-from")[0]
            #变卖公告
            detail_desc_temp_url = res.xpath("//div[@id='J_NoticeDetail']/@data-from")[0]
            # print(type(record_url_temp))
            detail_desc_url = 'https:' + detail_desc_temp_url
            item = {}
            #获取json文本，转化成element对象
            response = requests.get(detail_desc_url)
            # res = etree.HTML(response.text)
            #详情字段内容小于２０时，说明内容没有格式，直接返回响应文本
            # detail_desc_temp = response.text
            # print(detail_desc_temp)


            #详情字段为空时，提取拍卖公告中的数据
            res = etree.HTML(response.text)
            detail_desc_temp = res.xpath("//*//text()")
            # item = {}
            # item["detail_desc"] = detail_desc_temp
            # print(item["detail_desc"])
            if detail_desc_temp:
                # print(detail_desc_temp)
                detail_desc_1 = ','.join(detail_desc_temp).strip()
                ds = re.sub('\s', '', detail_desc_1).replace(',', '')
            #     # print(id,detail_desc)
            #     detail_desc_text2 = re.search(r"拍卖(.*?)二、", ds)
                detail_desc_text2 = re.search(r"一、(.*?)二、", ds)
                if detail_desc_text2:
                    detail_desc2 = ','.join(detail_desc_text2.group(1)).strip()
                    ds = re.sub('\s', '', detail_desc2).replace(',', '').replace('、', '')
                    item["detail_desc"] = ds
                    print(item["detail_desc"])

                    with conn.cursor() as cur2:
                        sql2 = "update `001_house_sum_info` set detail_desc = %s  where id = %s"
                        cur2.execute(sql2, (item["detail_desc"], id))
                        conn.commit()
                        conn.cursor().close()
                    print("**" * 50)
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