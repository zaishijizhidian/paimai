# -*- coding: utf-8 -*-
import json
import re

"""
    部分title中包含了房屋面积信息，可以先从这里获取部分house_area字段信息，共计4764条信息
"""
"""
    处理detail_desc中关于房屋面积的数据
"""

from lxml import etree

import requests
import datetime
# import uuid
from multiprocessing.pool import ThreadPool
import pymysql
from retrying import retry

def get_house_area():
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
        #处理标题中包含面积的数据
        #sql1 = "SELECT id,title, FROM `auction_house` WHERE title like '%土地%' and title like '%平方米%' and house_areahas is Null;"
        #处理详情描述中的面积数据
        # sql1 = "SELECT detail_desc FROM `auction_house` WHERE house_areahas is Null LIMIT 10;"
        # sql1 = "SELECT ID,title, detail_desc FROM DETAIL_DESC WHERE detail_desc is not NULL LIMIT 100;"
        # sql1 = "SELECT id,detail_desc from 01_new_auction_info where land_use_rights is Null limit 100;"
        sql1 = "SELECT id,detail_desc from 001_house_sum_info where house_card_num is Null;"
        cur1.execute(sql1)
        #设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        #获取此字段的所有信息
        results = cur1.fetchall()
        item = {}
        # print(results)
        for result in results:
            # print(111)
            #获取字典中的字段信息
            id = result["id"]
            # title = result["title"]
            detail_desc_temp = result["detail_desc"]
            if detail_desc_temp:
                detail_desc = re.sub('\s', '', detail_desc_temp).replace(',','')
                # print(id,detail_desc)

                #匹配房屋权证号 贵港房权证贵港市字第10077191号
                house_crefid_temp = re.search(r"[\u4e00-\u9fa5]{1,2}房权证(.*?字第.*?号)",detail_desc)
                if house_crefid_temp:
                    item["house_crefid"] = house_crefid_temp.group(0)
                else:
                    item["house_crefid"] = None

                # # 房屋产权证房号写入数据库
                # if house_crefid :
                #     # print(id,house_crefid)
                #     with conn.cursor() as cur2:
                #         sql2 = "update 01_new_auction_info set house_property_cardnum = %s where id = %s "
                #         # sql2 = "update new_auction_house set house_ = %s where id = %s  "
                #         cur2.execute(sql2, (house_crefid,id))
                #         conn.commit()
                #         conn.cursor().close()
                #         print("**" * 50)

                #匹配土地权证号
                land_crefid_temp = re.search(r"[\u4e00-\u9fa5]国用(.*?)第(.*?)号",detail_desc)
                if land_crefid_temp:
                    item["land_crefid"] = land_crefid_temp.group(0)
                else:
                    item["land_crefid"]= None
                if item["house_crefid"] or item["land_crefid"] :
                    print(id,str(item))
                    with conn.cursor() as cur3:
                        sql3 = "update 001_house_sum_info set house_card_num = %s where id = %s "
                        cur3.execute(sql3, (str(item), id))
                        conn.commit()
                        conn.cursor().close()
                        print("**" * 50)

# 多线程，为了提高效率
def multi():
    pool = ThreadPool(processes=8)
    pool.apply_async(get_house_area, ())
    pool.close()
    pool.join()



if __name__ == '__main__':
    starttime = datetime.datetime.now()
    multi()
    # get_house_area()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))