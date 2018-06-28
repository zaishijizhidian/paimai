# -*- coding: utf-8 -*-
import datetime
import json
import re
from multiprocessing.pool import ThreadPool

import pymysql
from lxml import etree

import requests

def get_detail_desc():
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
        """首先建一张new_bid_id的表，这里的bid_id与new_bid_record中的bid_id关联，形成一对多的联系"""
        sql1 = "SELECT id,itemUrl,detail_desc from 01_new_auction_info WHERE house_useage_detail is NULL ;"
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
            detail_desc = result["detail_desc"]
            itemurl = result["itemUrl"]
            # print(id, itemurl,detail_desc)

            if detail_desc:
                detail_desc_text1 = re.sub('\s', '', detail_desc).replace(',', '').replace('、', '')
                # print(id,detail_desc_text1)
                #获取房屋用途
                detail_desc_text = re.search(r"用途.*",detail_desc_text1)
                #获取房屋性质
                # detail_desc_text = re.search(r"性质.*",detail_desc_text1)
                if detail_desc_text:

                    detail_desc1 = detail_desc_text.group(0)
                else:
                    detail_desc1 = None
                if detail_desc1:
                    print(id,itemurl,detail_desc1)

                    with conn.cursor() as cur2:
                            sql2 = "update 01_new_auction_info set house_useage_detail = %s  where id = %s"
                            cur2.execute(sql2, (detail_desc1,id))
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