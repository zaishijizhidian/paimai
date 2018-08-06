# -*- coding: utf-8 -*-
from datetime import datetime
from multiprocessing.pool import ThreadPool

from elasticsearch import Elasticsearch
import elasticsearch.helpers
import pymysql, json, pytz
from bson import json_util, ObjectId
import json
from pymongo import MongoClient

def conn():

    es = Elasticsearch("http://elastic:Spiderman2018@es-cn-mp90n4agq000mftri.public.elasticsearch.aliyuncs.com:9200/", verify_certs=False,timeout = 60)
    # db = pymysql.connect(host='www.npacn.com', user='zxlh',password='8dMPjf1jIW8c', db='sipa_customer', local_infile=1, charset='utf8')
    db = pymysql.connect(host='192.168.11.251', user='root', password='youtong123', db='sipai', local_infile=1,
                         charset='utf8')
    # db = pymysql.connect(  # host='localhost',
    #     # host='192.168.11.251',
    #     host='data.npacn.com',
    #     port=3306,
    #     user='youtong',
    #     password='duc06LEQpgoP',
    #     # password='youtong123',
    #     # password='mysql',
    #     database='spiderman',
    #     # database='sipai_backup',
    #     charset='utf8',
    #     cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构

    # client = MongoClient('mongodb://dpuser:HxSwQT3AIPwMkIaD@10.50.86.179:27017')
    # mongo_db = client['dw']
    # coll = mongo_db['sipai']
    cursor = db.cursor()

    # sql = "select item_id,detail_desc from temp_detail_des "
    sql = "select * from sm_court "
    cursor.execute(sql)
    data = cursor.fetchall()
    for dataInfo in data:
        print(dataInfo)
        package = []
        row = {
            # "id": dataInfo[0],
            "name": dataInfo[1],
            "address":dataInfo[2] ,
            "phone":dataInfo[3]

        }
        # row = {
        #     "id": dataInfo[0],
        #     "asset_des": dataInfo[1].replace(' ','')
        # }

        package.append(row)
        action = [
            {
                '_op_type': 'index',
                '_index': "sm_court",
                '_type': "data",
                '_source': d
            }
            for d in package
            ]
        # print(111)
        elasticsearch.helpers.bulk(es, action)
        print("******"*20)
        print("插入elasticsearch成功")

# 多线程，为了提高效率
# def multi():
#     pool = ThreadPool(processes=8)
#     pool.apply_async(conn, ())
#     pool.close()
#     pool.join()

if __name__ == '__main__':
    # multi()
    conn()
