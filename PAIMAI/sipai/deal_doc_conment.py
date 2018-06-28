import json
import re
from multiprocessing.pool import ThreadPool

import pymysql
from lxml import etree

import requests


def get_detail_desc():
    conn = pymysql.connect(host='www.npacn.com',
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
        """首先建一张new_bid_id的表，这里的bid_id与new_bid_record中的bid_id关联，形成一对多的联系"""
        # sql1 = "SELECT id,itemUrl from `last_status(03)` where detail_desc = '';"
        sql1 = "SELECT id,detail_desc from `01_new_auction_info`  WHERE province = '浙江' AND detail_desc like '%法律文书%';"
        cur1.execute(sql1)
        # 设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        # 获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        for result in results:
            # print(111)
            # 获取字典中的字段信息
            id = result["id"]
            # bid_id = result["bid_id"]
            detail_desc_temp = result["detail_desc"]
            # print(id, itemurl)
            #（2015）温瓯商初字第01751号判决书。
            detail_desc = re.sub('\s', '', detail_desc_temp).replace(',', '')
            doc_content_temp = re.search(r"法律文书(.*?)第\d+号.*?书",detail_desc)
            if doc_content_temp:
                doc_content = doc_content_temp.group(0).replace(',','')
                print(doc_content)
                with conn.cursor() as cur2:
                    sql2 = "update `01_new_auction_info` set doc_content = %s  where id = %s"
                    cur2.execute(sql2, (doc_content, id))
                    conn.commit()
                    conn.cursor().close()
                    print("**" * 50)

# def multi():
#     pool = ThreadPool(processes=8)
#     pool.apply_async(get_detail_desc, ())
#     pool.close()
#     pool.join()

if __name__ == '__main__':

    # multi()
    get_detail_desc()
