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
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    # }
    item = {}
    response = requests.get(url,timeout=5)
    assert response.status_code == 200
    try:
        html = response.content.decode('gbk')
    # except UnicodeDecodeError:
    except Exception:
        html = response.text
    html_page = etree.HTML(html)
    # print(222)
    Location = html_page.xpath("//div[@id='itemAddress']//text()")[0].strip()
    # if Location:
    ls = Location.split(" ") if Location else None
    if ls:
        item["province"] = ls[0]
        item["city"] = ls[1] if len(ls) >= 2 else None
        item["town"] = ls[2] if len(ls) >= 3 else None
        item["detailAdrress"] = html_page.xpath("//div[@id='itemAddressDetail']//text()")[0].strip()
    else:
        item["province"] = None
        item["city"] = None
        item["town"] = None
        item["detailAdrress"] = None
        # print(town)
    return item



def get_province():
    # conn = pymysql.connect(#host='localhost',
    #                        host='192.168.11.251',
    #                        port=3306,
    #                        user='root',
    #                        password='youtong123',
    #                        # password='mysql',
    #                        database='sipai',
    #                        charset='utf8',
    #                        cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构
    conn = pymysql.connect(host='data.npacn.com', port=3306, user='youtong', password='duc06LEQpgoP', database='sipai',
                           charset='utf8',cursorclass=pymysql.cursors.DictCursor)

    with conn.cursor() as cur1:
        #筛选出起拍价格是评估价格两倍的数据，可以初步判断评估价格出现异常
        sql1 = "SELECT id,itemUrl FROM increment_data where id >476488 and id < 479448 ;"
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
                item = parse_url(itemurl)
            except Exception:
                item["province"] = None
                item["city"] = None
                item["town"] = None
                item["detailAdrress"] = None
            print(item)
            # print(type(coordinate))
            #将bid_id字段信息更新成唯一的uuid信息即titlt_id
            with conn.cursor() as cur2:
                sql2 = "update increment_data set province = %s,city = %s,town = %s,detailAdrress = %s where id = %s "
                cur2.execute(sql2, (item["province"],item["city"],item["town"],item["detailAdrress"],id))
                conn.commit()
                conn.cursor().close()
                print("**" * 50)

# 多线程，为了提高效率
# def multi():
#     pool = ThreadPool(processes=8)
#     pool.apply_async(get_province, ())
#     pool.close()
#     pool.join()



if __name__ == '__main__':
    starttime = datetime.datetime.now()
    # multi()
    get_province()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds

























