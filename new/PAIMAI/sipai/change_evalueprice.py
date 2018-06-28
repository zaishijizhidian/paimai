# -*- coding: utf-8 -*-
import json
from lxml import etree

import requests
import datetime
# import uuid
from multiprocessing.pool import ThreadPool
import pymysql
from retrying import retry

"""
由于版面信息不同，有些evalueprice和保证金的位置是对调的，因此需要将爬去的部分信息修改过来
"""

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
    div_list = html_page.xpath("//div[@class='pm-main clearfix']//span[@class='J_Price']/text()")
    evalueprice = div_list[3] if len(div_list)>3 else None
    print(evalueprice)
    return evalueprice



def get_evalueprice():
    conn = pymysql.connect(#host='localhost',
                           host='192.168.11.253',
                           port=3306,
                           user='root',
                           password='youtongmysql',
                           # password='mysql',
                           database='sipai',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构


    with conn.cursor() as cur1:
        sql1 = "select ID,itemUrl,deal_time from test_info WHERE deal_time > '2017-01-18';"
        cur1.execute(sql1)
        #设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        #获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        for result in results:
            #获取字典中的字段信息
            itemurl = result["itemUrl"]
            id = result["ID"]
            # coordinate = result["coordinate"]
            print(id,itemurl)
            evalueprice = parse_url(itemurl)
            # print(type(coordinate))
            #将bid_id字段信息更新成唯一的uuid信息即titlt_id
            with conn.cursor() as cur2:
                sql2 = "update test_info set evaluatePrice = %s where ID = %s "
                cur2.execute(sql2, (evalueprice,id))
                conn.commit()
                conn.cursor().close()
                print("**" * 50)

# 多线程，为了提高效率
def multi():
    pool = ThreadPool(processes=8)
    pool.apply_async(get_evalueprice, ())
    pool.close()
    pool.join()



if __name__ == '__main__':
    starttime = datetime.datetime.now()
    multi()
    # get_evalueprice()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))