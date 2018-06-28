# -*- coding: utf-8 -*-
import json
"""
    由于某些标的的title清洗的并不彻底．会出现一些带拍卖的括号，因此需要再进行一次清洗
"""

import pymysql
import requests
import datetime
# import uuid
from multiprocessing.pool import ThreadPool

def deal_title(title):
    title_status = title.split("）")[-1]


def get_title():
    conn = pymysql.connect(host='localhost',
                           #host='192.168.11.253',
                           port=3306,
                           user='root',
                           # password='youtongmysql',
                           password='mysql',
                           database='sipai_backup',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构


    with conn.cursor() as cur1:
        #筛选出起拍价格是评估价格两倍的数据，可以初步判断评估价格出现异常
        sql1 = "SELECT bid_id,itemUrl FROM test_info ip WHERE ip.evaluatePrice is not NULL and (ip.start_price+0)/(ip.evaluatePrice+0) > 2;"
        print(111)
        cur1.execute(sql1)
        #设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        #获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        for result in results:
            #获取字典中的字段信息
            itemurl = result["itemUrl"]
            bid_id = result["bid_id"]
            # coordinate = result["coordinate"]
            print(bid_id,itemurl)
            evalueprice = deal_title(itemurl)
            print(evalueprice)
            # print(type(coordinate))
            #将bid_id字段信息更新成唯一的uuid信息即titlt_id
            with conn.cursor() as cur2:
                sql2 = "update test_info set evaluatePrice = %s where bid_id = %s "
                cur2.execute(sql2, (evalueprice,bid_id))
                conn.commit()
                conn.cursor().close()
                print("**" * 50)

# 多线程，为了提高效率
def multi():
    pool = ThreadPool(processes=8)
    pool.apply_async(deal_title, ())
    pool.close()
    pool.join()



if __name__ == '__main__':
    starttime = datetime.datetime.now()
    multi()
    # get_evalueprice()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))