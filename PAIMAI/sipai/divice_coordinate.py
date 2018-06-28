# -*- coding: utf-8 -*-
import datetime
from multiprocessing.pool import ThreadPool

import pymysql

"""
将数据库中的坐标切分为经度和纬度

"""
def get_addr():
    conn = pymysql.connect(#host='localhost',
                           host='192.168.11.251',
                           port=3306,
                           user='root',
                           password='youtong123',
                           # password='mysql',
                           database='sipai',
                           # database='sipai_backup',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构


    with conn.cursor() as cur1:
        sql1 = "SELECT id,coordinate from 001_house_sum_info a WHERE a.Latitude is NULL and coordinate != 0;"
        # sql1 = "SELECT id,coordinate from 001_house_sum_info WHERE coordinate != 0;"

        cur1.execute(sql1)
        #设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        #获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        for result in results:
            #获取字典中的字段信息
            # address = result["title"]
            id = result["id"]
            coordinate = result["coordinate"]
            print(coordinate)
            # longtitude = result["Longtitude"]
            # latitude = result["Latitude"]
            # coordinate = latitude + ',' + longtitude
            print(id,coordinate)
            #经度，前面大的那部分
            longtitude = coordinate.split(',')[0]
            # #纬度，后面小的那部分
            latitude = coordinate.split(',')[1]
            # print(latitude,longtitude)
            # new_coordinate = latitude + ',' + longtitude
            #将现有的坐标分成经纬度
            with conn.cursor() as cur2:
                sql2 = "update 001_house_sum_info set Latitude = %s,Longtitude = %s where id = %s "
                # sql2 = "update 003_other_sum_info set Latitude = %s,Longtitude = %s where id = %s "
                cur2.execute(sql2, (latitude,longtitude,id))
            conn.commit()
            conn.cursor().close()
            print("**" * 50)

# 多线程，为了提高效率
# def multi():
#     pool = ThreadPool(processes=8)
#     pool.apply_async(get_addr, ())
#     pool.close()
#     pool.join()



if __name__ == '__main__':
    starttime = datetime.datetime.now()
    # multi()
    get_addr()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))