# -*- coding: utf-8 -*-
from datetime import datetime
from multiprocessing.pool import ThreadPool

from elasticsearch import Elasticsearch
import elasticsearch.helpers
import pymysql


def conn():
    es = Elasticsearch("http://elastic:Spiderman2018@es-cn-mp90n4agq000mftri.public.elasticsearch.aliyuncs.com:9200/",
                       verify_certs=False, timeout=60)

    db = pymysql.connect(  # host='localhost',
        # host='192.168.11.251',
        host='data.npacn.com',
        port=3306,
        user='youtong',
        password='duc06LEQpgoP',
        # password='youtong123',
        # password='mysql',
        database='spiderman',
        # database='sipai_backup',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)

    cursor = db.cursor()
    for n in range(701):
        m = n * 1000
        sql = "select * from sm_document_copy limit {},1000".format(m)
        cursor.execute(sql)
        data = cursor.fetchall()

        for dataInfo in data:
            # print(dataInfo)
            package = []
            #在sm_document_copy中适用，格式是dict
            row = {
                "id": dataInfo["id"],
                "create_by": dataInfo["create_by"],
                "create_date": dataInfo["create_date"],
                "update_by": dataInfo["update_by"],
                "update_date": dataInfo["update_date"],
                "del_flag": dataInfo["del_flag"],
                "obligors": dataInfo["obligors"],
                "creditors": dataInfo["creditors"],
                "court": dataInfo["court"],
                "case_no": dataInfo["case_no"],
                "doc_type": dataInfo["doc_type"],
                "doc_content": dataInfo["doc_content"],
                "doc_result": dataInfo["doc_result"],

                "doc_money": dataInfo["doc_money"],
                "doc_assets": dataInfo["doc_assets"],
                "doc_source": dataInfo["doc_source"],

                "doc_province": dataInfo["doc_province"],
                "doc_city": dataInfo["doc_city"]

            }


            package.append(row)
            action = [
                {
                    '_op_type': 'index',
                    '_index': "sm_document",
                    '_type': "data",
                    '_source': d
                }
                for d in package
                ]
            elasticsearch.helpers.bulk(es, action)
            print("******"*20)
            print("插入elasticsearch成功")

# 多线程，为了提高效率
def multi():
    pool = ThreadPool(processes=8)
    pool.apply_async(conn, ())
    pool.close()
    pool.join()

if __name__ == '__main__':
    starttime = datetime.now()
    multi()
    # conn()
    endtime = datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))
