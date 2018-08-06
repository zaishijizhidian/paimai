# -*- coding: utf-8 -*-
from datetime import datetime
from multiprocessing.pool import ThreadPool

from elasticsearch import Elasticsearch
import elasticsearch.helpers
import pymysql


def conn():
    # es = Elasticsearch("http://elastic:Spiderman2018@es-cn-mp90n4agq000mftri.public.elasticsearch.aliyuncs.com:9200/",
    #                    verify_certs=False, timeout=60)
    # db = pymysql.connect(host='192.168.11.251', user='root', password='youtong123', db='spiderman', local_infile=1,
    #                      charset='utf8')
    es = Elasticsearch("http://12.33.0.71:9200/", verify_certs=False,timeout = 60)
    db = pymysql.connect(host='localhost', user='jackfull', password='fz1616', db='sipai', local_infile=1,
                         charset='utf8')

    cursor = db.cursor()
    for n in range(0,701):
        m = n * 1000
        k = m + 1000
        sql = "select * from new_sm_document where uuid > {} and uuid <= {}".format(m,k)
        data = cursor.fetchall()

        for dataInfo in data:
            # print(dataInfo)
            package = []

            row = {
                "uuid": dataInfo[0],
                "id": dataInfo[1],
                "create_by": dataInfo[2],
                "create_date": dataInfo[3],
                "update_by": dataInfo[4],
                "update_date": dataInfo[5],
                "del_flag": dataInfo[7],
                "obligors": dataInfo[8],
                "creditors": dataInfo[9],
                "court": dataInfo[10],
                "case_no": dataInfo[11],
                "doc_type": dataInfo[12],
                "doc_content": dataInfo[13],
                "doc_result": dataInfo[14],

                "doc_money": dataInfo[15],
                "doc_assets": dataInfo[16],
                "doc_source": dataInfo[17],

                "doc_province": dataInfo[18],
                "doc_city": dataInfo[19]
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
# def multi():
#     pool = ThreadPool(processes=8)
#     pool.apply_async(conn, ())
#     pool.close()
#     pool.join()

if __name__ == '__main__':
    starttime = datetime.now()
    # multi()
    conn()
    endtime = datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))
