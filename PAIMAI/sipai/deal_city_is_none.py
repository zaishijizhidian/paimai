# -*- coding: utf-8 -*-
import json
"""
    由于页面类型不一致，造成资产信息表中有些省市区的信息不完全，需要重新进行爬取,更改了Location中列表索引，由第一个改为第三个
"""

from lxml import etree

import requests
import datetime
# import uuid
from multiprocessing.pool import ThreadPool
import pymysql
from retrying import retry


@retry(stop_max_attempt_number=4)
def parse_url(url):
    # print(111)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    }

    response = requests.get(url, headers=headers, timeout=5)
    assert response.status_code == 200
    try:
        html = response.content.decode('gbk')
    # except UnicodeDecodeError:
    except Exception:
        html = response.text
    html_page = etree.HTML(html)
    # print(222)
    Location = html_page.xpath("//div[@class='detail-common-text']/text()")
    # Location_text = Location[2].strip()
    Location_text1 = Location[-1].strip()
    print(Location)
    print(Location_text1)
    lt = None
    if Location_text1:
        lt = Location_text1
    else:
        Location_text2 = Location[2].strip()
        print("******"*20)

        if Location_text2:
            lt = Location_text2
            # print(lt)
        else:
            lt = Location[5].strip()
            print("======"*20)
    if lt:
        ls = lt.split(" ")
        province = ls[0][-2:]
        # print(province)
        city = ls[1] if len(ls) >= 2 else None
        # print(city)
        town =ls[2] if len(ls) >= 3 else None
        # print(town)
        return province,city,town



def get_province():
    conn = pymysql.connect(#host='localhost',
                           host='192.168.11.251',
                           port=3306,
                           user='root',
                           password='youtong123',
                           # password='mysql',
                           database='sipai',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构


    with conn.cursor() as cur1:
        #筛选出起拍价格是评估价格两倍的数据，可以初步判断评估价格出现异常
        sql1 = "SELECT id,itemUrl FROM 00_house_sum_info hsi where hsi.city is not NULL;"
        # print(111)
        cur1.execute(sql1)
        #设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        #获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        for result in results:
            #获取字典中的字段信息
            itemurl = result["itemUrl"]
            id = result["id"]
            # coordinate = result["coordinate"]
            print(id,itemurl)
            try:
                province,city,town = parse_url(itemurl)
            except Exception:
                province = None
                city = None
                town = None
            print(province, city, town)
            # print(type(coordinate))
            #将bid_id字段信息更新成唯一的uuid信息即titlt_id
            # with conn.cursor() as cur2:
            #     sql2 = "update 00_house_sum_info set province = %s,city = %s,town = %s where id = %s "
            #     cur2.execute(sql2, (province,city,town,id))
            #     conn.commit()
            #     conn.cursor().close()
            #     print("**" * 50)

# 多线程，为了提高效率
def multi():
    pool = ThreadPool(processes=8)
    pool.apply_async(get_province, ())
    pool.close()
    pool.join()



if __name__ == '__main__':
    starttime = datetime.datetime.now()
    multi()
    # get_province()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds

























