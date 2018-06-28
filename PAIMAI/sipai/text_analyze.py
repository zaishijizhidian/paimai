import json
import re

import pymysql
from aip import  AipNlp




def get_detail_desc():
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
        #处理标题中包含有证面积的数据
        sql1 = "SELECT id,title,detail_desc FROM 01_new_auction_info limit 100;"
        #处理详情描述中的面积数据
        # sql1 = "SELECT detail_desc FROM `auction_house` WHERE house_areahas is Null LIMIT 10;"
        # sql1 = "SELECT ID,title, detail_desc FROM DETAIL_DESC WHERE detail_desc is not NULL LIMIT 100;"
        # sql1 = "SELECT id,detail_desc from new_auction_house where house_areahas is not Null;"
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
            title = result["title"]
            # house_areahas = result["house_areahas"]
            detail_desc_temp = result["detail_desc"]
            if detail_desc_temp:
                detail_desc = re.sub('\s', '', detail_desc_temp).replace(',', '').replace('、', '')
                client = get_aip()
                try:
                    tag = client.keyword(title, detail_desc)
                    # tag = client.topic(title,detail_desc)
                except Exception:
                    tag = None
                    print(id,detail_desc)
                    pass
                    # s = detail_desc.encode(encoding='utf-8')
                    # detail_desc1 = json.loads(s)
                    # detail_desc = str(detail_desc1, encoding = "utf-8")
                    # tag = client.keyword(title,detail_desc)
                    # tag = client.topic(title, detail_desc)

                print(id,tag)




def get_aip():
    APP_ID = '10960654'
    API_KEY = 'x76K8BWD9cGFqXEmo94nMc33'
    SECRET_KEY = 'mS3PBowxdim9dCLevUjpIeEzRB7nEkqd'

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    return client



if __name__ == '__main__':
    get_detail = get_detail_desc()
    # print(get_detail)












