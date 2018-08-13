# -*- coding: utf-8 -*-
import json
from lxml import etree
import requests
import datetime
import html5lib
from multiprocessing.pool import ThreadPool
import pymysql
import pandas as pd

def parse_table(url):
    res = requests.get(url)
    response = etree.HTML(res.text)
    # 标的物详情描述,正则匹配（异步加载）
    detail = response.xpath("//div[@class='detail-common-text clearfix']/@data-from")
    # 获取json数据链接
    detail_url = 'https:' + detail[0]
    resp = requests.get(detail_url)
    data = resp.text
    data = str(data).replace("var desc='", "").replace("';", '')
    # df = pd.read_html(url,index_col='Year',header=0,parse_dates=True)[0]
    #pandas读取html页面信息
    if "table" in data:
        table = pd.read_html(data)[0]
        print(table)

        df_temp = pd.DataFrame(table)
        if len(df_temp) < 5:
            df = df_temp.stack().unstack(0)
        else:
            df = df_temp
        # print(df)

        try:
            bd = df[(df[0] == '拍品所有人') | (df[0] == '房屋所有权人') | (df[0] == '标的所有人') | (df[0] == '土地使用权人')].index
            # bd = df[(df[0].str.contains('所有人', '使用权','所有权', na=False))].index
            # bd = eval(bd)
            doc = df[(df[0] == '执行所依据的法律文书') | (df[0] == '执行案号')].index
            # doc = df[(df[0].str.contains('执行', '文书', na=False))].index
            # doc = eval(doc)
            # card_num = df[(df[0] == '产权证号') | (df[0] == '《房屋所有权证》证号') | (df[0] == '权证情况')].index
            # card_num = df[(df[0].str.contains('权证', na=False))].index
            # card_num = eval(card_num)
            type = df[(df[0] == '房屋用途及土地性质') | (df[0] == '用途') | (df[0] == '标的现状') | (df[1] == '房屋用途及土地性质') | (df[1] == '用途')].index
            # type = df[(df[0].str.contains('用途', regex=True))].index
            # area = df[(df[0].str.contains('面积', na=False))].index
            # area = eval(area)
        except Exception as e:
            print("error",e)
            return None, None, None
        else:
            return df.ix[bd][1], df.ix[doc][1], df.ix[type]
        #     return bd,doc,card_num,type,area
    else:
        return None,None,None

def get_table():
    conn = pymysql.connect(host='localhost',
        # host='192.168.11.251',
        port=3306,
        user='root',
        # password='youtong123',
        password='mysql',
        database='sipai',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构
    with conn.cursor() as cur1:
    # sql1 = "SELECT id,title from land_sum_info a WHERE a.confidence is not Null;"
        sql1 = "SELECT id,title from test_info limit 10;"
        cur1.execute(sql1)
        # 设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        # 获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        for result in results:
        # 获取字典中的字段信息
            item_url = result["itemUrl"]
            id = result["id"]
    # engine = create_engine('mysql+pymysql://root:youtong123@192.168.11.251:3306/sipai')
    #     # sql1 = "SELECT id,title from land_sum_info a WHERE a.confidence is not Null;"
    # sql1 = "SELECT id,itemUrl from test;"
    # data = pd.read_sql(sql1,con=conn)
    # # print(data)



        # data2 = pd.concat(auction_people)
        # print(data2)
        # print(type(auction_people))
        # print(auction_people)
        # aa = pd.DataFrame(auction_people)
        # print(aa)
        # print(type(auction_people))
        # item = {}
        # item["bd"] = auction_people
        # item["doc"] = jdu_doc_number
        # item["house_type"] = house_useage_detail
        # 获取字典中的字段信息
        # url = result["itemUrl"]
        # # print(url)
        # id = result["id"]
        # id = pd.DataFrame(id)
        # coordinate = result["coordinate"]
        # print(id,address)

        # print(lat,lng,confidence)
        # 数据库中的坐标是按照经纬度的顺序来的(先大后小)，但是在真正查询的时候是按照先维度后进度的顺序来的（先小后大）
        # bd, doc, house_type = parse_table(url)

      # })
        #
        # item["bd"] = bd
        # # print(type(item["bd"]))
        # item["doc"] = doc
        # item["card_num"] = card_num
        # item["house_type"] = house_type
        # # print(type(item["house_type"]))
        # item["area"] = area
        # print(item)

        # print(coordinate)
        # 将bid_id字段信息更新成唯一的uuid信息即titlt_id
        # with conn.cursor() as cur2:
        #     sql2 = "update 001_house_sum_info set house_useage_detail= %s,auction_people=%s,jdu_doc_number=%s where id = %s"
        #     cur2.execute(sql2, (house_type,bd,doc,id))
        #     print(id, house_type,bd,doc)
        #     conn.commit()
        #     conn.cursor().close()
        #     print("**" * 50)


# 多线程，为了提高效率
# def multi():
#     pool = ThreadPool(processes=8)
#     pool.apply_async(get_addr, ())
#     pool.close()
#     pool.join()


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    # multi()
    get_table()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))
    # -*- coding: utf-8 -*-