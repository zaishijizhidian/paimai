# -*- coding: utf-8 -*-
import json

import requests
import datetime

from multiprocessing.pool import ThreadPool
import pymysql


def get_latlng(addr):
    ak='Ml0kB3WSGGjyIo8V2PznW0wjUo2xWQeH'
    url='http://api.map.baidu.com/geocoder/v2/'
    # url='http://api.map.baidu.com/geocoder'

    payload={
    'output':'json',
    'ak':ak,
    # 'coord_type':'bd09',
    # 'callback':'showLocation',
    'address':addr,
    'src':"经纬度"
    }
    # try:
    response=requests.get(url,params=payload)
    # print response
    contents=response.content.decode('utf-8')
    # print type(content)
    json_result=json.loads(contents)
    # print(eval(contents))
    # print(type(json_result["status"]))

    if json_result["status"] == 0:
        coordinate = json_result["result"]["location"]
        # print(coordinate)
        confidence=json_result['result']['confidence']
        #经度坐标,进度的坐标要比维度的大
        lng = coordinate["lng"]
        # 纬度坐标，较小的那个坐标
        lat = coordinate["lat"]



    else:

        confidence = None
        lng = None
        lat = None

    return confidence,lat,lng




def get_addr():
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
        # sql1 = "SELECT id,title from land_sum_info a WHERE a.confidence is not Null;"
        sql1 = "SELECT id,title from 003_other_sum_info a WHERE a.coordinate = '0';"
        cur1.execute(sql1)
        #设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        #获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        for result in results:
            #获取字典中的字段信息
            address = result["title"]
            id = result["id"]
            # coordinate = result["coordinate"]
            # print(id,address)
            confidence,lat,lng,= get_latlng(address)
            # print(lat,lng,confidence)
            #数据库中的坐标是按照经纬度的顺序来的(先大后小)，但是在真正查询的时候是按照先维度后进度的顺序来的（先小后大）
            coordinate = str(lng)  + ',' + str(lat)

            # print(coordinate)
            #将bid_id字段信息更新成唯一的uuid信息即titlt_id
            with conn.cursor() as cur2:
                sql2 = "update 003_other_sum_info set coordinate = %s,Latitude = %s, Longtitude = %s,confidence = %s where id = %s "
                cur2.execute(sql2, (coordinate,lat,lng,confidence,id))
                print(id,coordinate,confidence)
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