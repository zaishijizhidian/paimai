# -*- coding: utf-8 -*-
import json

import requests
import datetime
# import uuid
from multiprocessing.pool import ThreadPool
import pymysql

def get_addr():
    conn = pymysql.connect(#host='localhost',
                           host='192.168.11.253',
                           port=3306,
                           user='root',
                           password='youtongmysql',
                           database='sipai',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构


    with conn.cursor() as cur1:
        sql1 = "SELECT id,Longtitude,Latitude,confidence from new_auction_info a WHERE a.confidence is not NULL;"
        cur1.execute(sql1)
        #设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        #获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        for result in results:
            #获取字典中的字段信息
            id = result["id"]
            # coordinate = result["coordinate"]
            lng = result["Longtitude"]
            lat = result["Latitude"]
            # confidence = result["confidence"]
            # print(lat,lng,confidence)
            coordinate = lat + "," + lng
            # print(type(coordinate))
            #将bid_id字段信息更新成唯一的uuid信息即titlt_id
            with conn.cursor() as cur2:
                sql2 = "update new_auction_info set coordinate = %s, Latitude = %s,Longtitude = %s where id = %s "
                cur2.execute(sql2, (coordinate,lat,lng,id))
                print(coordinate)
                conn.commit()
                conn.cursor().close()
                print("**" * 50)

# 多线程，为了提高效率
def multi():
    pool = ThreadPool(processes=8)
    pool.apply_async(get_addr, ())
    pool.close()
    pool.join()



if __name__ == '__main__':
    starttime = datetime.datetime.now()
    multi()
    # get_addr()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))