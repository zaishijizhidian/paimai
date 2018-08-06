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
    db = pymysql.connect(host='192.168.11.251', user='root', password='youtong123', db='sipai', local_infile=1,
                         charset='utf8')

    cursor = db.cursor()

    sql = "select * from sm_auction "
    cursor.execute(sql)
    data = cursor.fetchall()
    for dataInfo in data:
        print(dataInfo)
        package = []
        row = {
            "id": dataInfo[1],
            "create_by": dataInfo[2],
            "create_date": dataInfo[3],
            "update_by": dataInfo[4],
            "update_date": dataInfo[5],
            "del_flag": dataInfo[7],
            "court": dataInfo[8],
            "contacts": dataInfo[9],
            "phone_num": dataInfo[10],
            "asset_name": dataInfo[11],
            "asset_address": dataInfo[12],
            "longitude": dataInfo[13],
            "latitude": dataInfo[14],
            "asset_type": dataInfo[15],

            "asset_no": dataInfo[16],
            "evaluate_price": dataInfo[17],
            "starting_price": dataInfo[18],

            "deal_price": dataInfo[19],
            "report_no": dataInfo[20],
            "asset_holders": dataInfo[21],
            "case_no": dataInfo[22],
            "trade_date": dataInfo[23],

            "auction_type": dataInfo[24],
            "auction_status": dataInfo[25],
            "legal_remark": dataInfo[26],
            "asset_des": dataInfo[27],
            "province": dataInfo[28],
            "city": dataInfo[29],
            "source_name": dataInfo[20],
            "source_url": dataInfo[31],
            "location": dataInfo[32]

        }
        # print(row)
        package.append(row)
        action = [
            {
                '_op_type': 'index',
                '_index': "sm_auction_test",
                '_type': "data",
                '_source': d
            }
            for d in package
            ]
        # print(111)
        elasticsearch.helpers.bulk(es, action)
        print("******"*20)
        print("插入elasticsearch成功")


if __name__ == '__main__':
    # multi()
    conn()
