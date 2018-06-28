# -*- coding: utf-8 -*-
import json

import pymysql
import time

import re


def get_addr():
    conn = pymysql.connect(#host='localhost',
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
                           cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构


    with conn.cursor() as cur1:
        t1 = time.time()
        for n in range(700):
            m = n*1000
            sql1 = """SELECT id, doc_assets from sm_document_copy limit {},1000 """.format(m)
            cur1.execute(sql1)
            #设定游标从第一个开始移动
            cur1.scroll(0, mode='absolute')
            #获取此字段的所有信息
            results = cur1.fetchall()
            # print(results)

            for demo_sent1 in results:
                id = demo_sent1['id']
                demos = demo_sent1['doc_assets']
                # print(demos)

                pattern = re.compile(r'{(.*?)\}\]')
                try:
                    ds = re.search(pattern, demos).group(1)
                except Exception as e:
                    print(e)
                    pass
                else:
                    a = ds.replace('{', '[').replace('}', ']').replace('None','null')
                    strs = '[{' + a + "}]"
                    # print(strs)
                    with conn.cursor() as cur2:
                        sql2 = "update sm_document_copy set doc_assets = %s where id = %s "
                        cur2.execute(sql2, (strs, id))
                        conn.commit()
                        conn.cursor().close()
                        t2 = time.time()
                        print(t2-t1)
                        print(id, strs)
                        print("**" * 50)



if __name__ == '__main__':
    get_addr()