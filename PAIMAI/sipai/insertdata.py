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
    # client = MongoClient('mongodb://dpuser:HxSwQT3AIPwMkIaD@10.50.86.179:27017')
    # mongo_db = client['dw']
    # coll = mongo_db['sipai']
    cursor = db.cursor()

    sql = "select item_id,detail_desc from temp_detail_des "
    cursor.execute(sql)
    data = cursor.fetchall()

    for dataInfo in data:
        # print(dataInfo)
        package = []

        # row = {
        #     "id": dataInfo[0],
        #     "create_by": dataInfo[1],
        #     "create_date":dataInfo[2] ,
        #     "update_by":dataInfo[3] ,
        #     "update_date": dataInfo[4],
        #     "del_flag": dataInfo[6],
        #     "court": dataInfo[7],
        #     "contacts":dataInfo[8] ,
        #     "asset_name": dataInfo[9],
        #     "asset_address": dataInfo[10],
        #     "longitude": dataInfo[11],
        #     "latitude": dataInfo[12],
        #     "asset_type":dataInfo[13],
        #
        #     "asset_no": dataInfo[14],
        #     "evaluate_price": dataInfo[15],
        #     "starting_price": dataInfo[16],
        #
        #     "deal_price": dataInfo[17],
        #     "report_no": dataInfo[18],
        #     "asset_holders": dataInfo[19],
        #     "case_no": dataInfo[20],
        #     "trade_date": dataInfo[21],
        #
        #     "auction_type":dataInfo[22] ,
        #     "auction_status":dataInfo[23] ,
        #     "legal_remark":dataInfo[24],
        #     "asset_des":dataInfo[25],
        #     "province":dataInfo[26],
        #     "city":dataInfo[27],
        #     "source_name":dataInfo[28],
        #     "source_url":dataInfo[29]
        #
        #
        # }
        row = {
            "id": dataInfo[0],
            "asset_des": dataInfo[1].replace(' ','')
        }

        package.append(row)
        action = [
            {
                '_op_type': 'index',
                '_index': "detail_desc",
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
