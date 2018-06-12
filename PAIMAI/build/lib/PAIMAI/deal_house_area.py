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
    #
    conn = pymysql.connect( host='www.npacn.com',
        # host='192.168.11.251',
        port=3306,
        # user='root',
        user='zxlh',
        # password='youtong123',
        password='8dMPjf1jIW8c',
        database='sipa_customer',
        # database='sipai',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构


    with conn.cursor() as cur1:
        #处理标题中包含有证面积的数据
        # sql1 = "SELECT id,detail_desc FROM 01_new_auction_info WHERE detail_desc like '%使用权面积%'and id > 297585;"
        #处理详情描述中的面积数据
        # sql1 = "SELECT detail_desc FROM `auction_house` WHERE house_areahas is Null LIMIT 10;"
        # sql1 = "SELECT ID,title, detail_desc FROM DETAIL_DESC WHERE detail_desc is not NULL LIMIT 100;"
        sql1 = "SELECT id,detail_desc from 01_new_auction_info limit 100;"
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
            # house_areahas = result["house_areahas"]
            detail_desc_temp = result["detail_desc"]
            if detail_desc_temp:
                detail_desc = re.sub('\s', '', detail_desc_temp).replace(',','').replace('：','')
                # print(id,detail_desc)
                #匹配有证/建筑面积和无证／土地面积，先把有证／建筑／土地面积的部分匹配出来
                house_area_has_temp = re.findall(r"建筑面积.*?([0-9]+\.[0-9]{1,2})平方米|建筑面积.*?([0-9]+\.[0-9]{1,2})㎡", detail_desc)
                house_area_has = house_area_has_temp if house_area_has_temp else None
                land_area_has_temp = re.findall(r"使用权面积[\u4e00-\u9fa5]?([0-9]+\.[0-9]{1,2})平方米|使用权面积[\u4e00-\u9fa5]?([0-9]+\.[0-9]{1,2})㎡", detail_desc)
                land_area_has = land_area_has_temp if land_area_has_temp else None

                #由于建筑面积提取的结果中由部分重复的数据，需要将列表结果去重
                if house_area_has :
                    house_area_has_set = list(set(house_area_has))
                    house_area_str = [''.join(house_area) for house_area in house_area_has_set]
                    house_area_num = [float(house_area_float) for house_area_float in house_area_str]
                    house_area_sum = round(sum(house_area_num),2)
                    print(id,house_area_has_set,house_area_sum)
                    # with conn.cursor() as cur2:
                    #     sql2 = "update 01_new_auction_info set total_house_area = %s where id = %s  "
                    #     cur2.execute(sql2, (house_area_sum,id))
                    #     conn.commit()
                    #     # conn.cursor().close()
                    #     print("**" * 50)

                        # house_area_sum = sum(list(map(float,list(map(lambda x:x[1],house_area_has_set)))))
                if land_area_has:
                    land_area_has_set = list(set(land_area_has))
                    land_area_str = [''.join(land_area) for land_area in land_area_has_set]
                    land_area_num = [float(land_area_float) for land_area_float in land_area_str]
                    land_area_sum = round(sum(land_area_num),2)
                    print(id,land_area_has_set,land_area_sum)
                    # with conn.cursor() as cur3:
                    #     sql2 = "update 01_new_auction_info set total_land_area = %s where id = %s  "
                    #     cur3.execute(sql2, (land_area_sum,id))
                    #     conn.commit()
                    #     conn.cursor().close()
                    #     print("**" * 50)
                # house_area_no = re.findall(r"([0-9]+\.[0-9]{1,2})平方米", detail_desc)
                # # house_area_no = house_area_no_temp.group(1) if house_area_no_temp else None
                # if house_area_no:
                #     print(id,house_area_no)
                # house_area_temp1 = re.search(title_pattern1,detail_desc)
                # house_area_temp2 = re.search(title_pattern2,detail_desc)
                # # house_area_temp2 = re.findall(title_pattern1,detail_desc)
                # if house_area_temp1:
                #     house_area = house_area_temp1.group(1)
                #     # house_area = house_area_temp1 if house_area_temp1 else None
                # else:
                #     house_area = house_area_temp2.group(0) if house_area_temp2 else  None
                # print(id,house_area)


# 多线程，为了提高效率
# def multi():
#     pool = ThreadPool(processes=8)
#     pool.apply_async(get_house_area, ())
#     pool.close()
#     pool.join()



if __name__ == '__main__':
    starttime = datetime.datetime.now()
    # multi()
    get_house_area()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))

    # 匹配标题中无小数点的房屋面积
    # title_pattern = re.search(r"([0-9]+)㎡|([0-9]+)平方米", detail_desc)
    # house_area = title_pattern.group(1) if title_pattern else None
    # if house_area:
    #     print(id,detail_desc,house_area)
    # 匹配有２个小数点的房屋面积
    # title_pattern1 = re.search(r"([0-9]+\.[0-9]{1,2})㎡|([0-9]+\.[0-9]{1,2})平方米",detail_desc)
    # house_area_has = title_pattern1.group(1) if title_pattern1 else None
    # if house_area_has:
    #     print(id,detail_desc,house_area_has)
    # 匹配无小数点的房屋面积
    # title_pattern2 = re.compile('([0-9]+)㎡')
    # title_pattern2 = re.compile('([0-9]+\.[0-9]{1,2})平方米') or re.compile('([0-9])平方米')
    # title_pattern2 = re.compile('([0-9]+)平方米')
    # title_pattern1 = re.compile('.*?([0-9]+\.[0-9]{1,2}).*?')
    # house_area_temp1 = re.search(r"面积(.*?)平方米|㎡", detail_desc)



    # 然后把带有２个小数点的数字提取出来
    # if house_area_has :
    #     house_area_has1 =re.search(r".*?([0-9]+\.[0-9]{1,2}).*?", house_area_has)
    #     house_area_no1 =re.search(r".*?([0-9]+\.[0-9]{1,2}).*?", house_area_no)
    #
    #     house_area_has2 = house_area_has1.group(1) if house_area_has1 else None
    #
    #     house_area_no2 = house_area_no1.group(1) if house_area_no1 else None
    #
    #     total_area_temp = float(house_area_has1.group(1)) + float(house_area_no1.group(1)) if house_area_has1 and house_area_no1 else None
    #     total_area = str(round(total_area_temp,2)) if total_area_temp else  None
    # print(id,detail_desc)
    # if house_area_has:
    #     for house_area in house_area_has:
    #         house_area_str = ''.join(house_area)
    #         # house_area1 = house_area[1]
    #         # house_area2 = house_area[2]
    #         print(id,house_area_str)
    # if land_area_has:
    #     for land_area in land_area_has:
    #         land_area_str = ''.join(land_area)
    #         # land_area1 = land_area[1]
    #         # land_area2 = land_area[2]
    #         print(id,land_area_str)
                        # sql2 = "update new_auction_house set land_property_cardnum = %s,house_property_cardnum = %s where id = %s "
                        # sql2 = "update new_auction_house set house_areahas = %s,house_areano = %s,total_area = %s where id = %s  "
