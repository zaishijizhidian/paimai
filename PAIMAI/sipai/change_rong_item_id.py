# -*- coding: utf-8 -*-
import datetime
from multiprocessing.pool import ThreadPool

import pymysql

def get_item_id():
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
        #筛选出起拍价格是评估价格两倍的数据，可以初步判断评估价格出现异常
        sql1 = "SELECT id, bid_id,item_id  FROM `00_house_sum_info` ORDER BY `deal_time` DESC LIMIT 30000 ;"
        print(111)
        cur1.execute(sql1)
        #设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        #获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        for result in results:
            #获取字典中的字段信息
            id = result["id"]
            item_id = result["item_id"]
            bid_id = result["bid_id"]
            # coordinate = result["coordinate"]
            print(bid_id,item_id)
            if len(bid_id) < len(item_id):
                bid_id,item_id = item_id,bid_id
            # print(evlueprice)
            # print(type(coordinate))
            #将bid_id字段信息更新成唯一的uuid信息即titlt_id
            with conn.cursor() as cur2:
                sql2 = "update `00_house_sum_info` set bid_id = %s,item_id = %s where id = %s "
                cur2.execute(sql2, (bid_id,item_id,id))
                conn.commit()
                conn.cursor().close()
                print("**" * 50)

# 多线程，为了提高效率
def multi():
    pool = ThreadPool(processes=8)
    pool.apply_async(get_item_id, ())
    pool.close()
    pool.join()



if __name__ == '__main__':
    starttime = datetime.datetime.now()
    multi()
    # get_item_id()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds



