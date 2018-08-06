# -*- coding: utf-8 -*-
from datetime import datetime
from multiprocessing.pool import ThreadPool

from elasticsearch import Elasticsearch
import elasticsearch.helpers
import pymysql


def conn():
    es = Elasticsearch("http://elastic:Spiderman2018@es-cn-mp90n4agq000mftri.public.elasticsearch.aliyuncs.com:9200/",
                       verify_certs=False, timeout=60)
    db = pymysql.connect(host='192.168.11.251', user='root', password='youtong123', db='spiderman', local_infile=1,
                         charset='utf8')

    cursor = db.cursor()
    for n in range(701):
        m = n * 1000
        sql = "select * from new_sm_document limit {},1000".format(m)
        cursor.execute(sql)
        data = cursor.fetchall()

        for dataInfo in data:
            # print(dataInfo)
            package = []

            row = {
                    "id": dataInfo[0],
                    "create_by": dataInfo[1],
                    "create_date": dataInfo[2],
                    "update_by": dataInfo[3],
                    "update_date": dataInfo[4],
                    "del_flag": dataInfo[6],
                    "obligors": dataInfo[7],
                    "creditors": dataInfo[8],
                    "court": dataInfo[9],
                    "case_no": dataInfo[10],
                    "doc_type": dataInfo[11],
                    "doc_content": dataInfo[12],
                    "doc_result": dataInfo[13],

                    "doc_money": dataInfo[14],
                    "doc_assets": dataInfo[15],
                    "doc_source": dataInfo[16],

                    "doc_province": dataInfo[17],
                    "doc_city": dataInfo[18]
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
