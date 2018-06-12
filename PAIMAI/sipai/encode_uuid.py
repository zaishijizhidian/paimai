# -*- coding: utf-8 -*-
import datetime
import uuid
from multiprocessing.pool import ThreadPool
import pymysql

def uid():
    conn = pymysql.connect(host='192.168.11.251',
                           # host = 'localhost',
                           port=3306,
                           user='root',
                           password='youtong123',
                           # password='mysql',
                           # database='sipai',
                           database='sipai',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构


    with conn.cursor() as cur1:
        # sql1 = "select ID,title from land_sum_info;"
        sql1 = "select ID,title from land_sum_info;"
        cur1.execute(sql1)
        #设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        #获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        for result in results:
            #获取字典中的字段信息
            title = result["title"]
            # itemUrl = result["itemUrl"]
            id = result["ID"]
            # print(id,itemUrl)
            #生成唯一标识的uuid信息
            u = uuid.uuid5(uuid.NAMESPACE_OID,title)
            #生成12位的整数数字
            title_id = u.time_low
            print(title_id)

            #将bid_id字段信息更新成唯一的uuid信息即title_id
            with conn.cursor() as cur2:
                sql2 = "update land_sum_info set item_id = %s where ID = %s "
                cur2.execute(sql2, (title_id, id))
                conn.commit()
                conn.cursor().close()
                print("**" * 50)

# def main():
#     title_id = uid()
#     print("更新成功")


# 多线程，为了提高效率
def multi():
    pool = ThreadPool(processes=8)
    pool.apply_async(uid, ())
    pool.close()
    pool.join()


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    # main()
    multi()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))
