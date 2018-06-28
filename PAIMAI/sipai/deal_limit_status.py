
import datetime
import re
from multiprocessing.pool import ThreadPool

from lxml import etree
import json
#from  sipai.deal_auction_people import repalce_auction_people
from retrying import retry
import pymysql
import requests

import pandas as pd
def parse_table(url):
    res = requests.get(url)
    response = etree.HTML(res.text)
    # 标的物详情描述,正则匹配（异步加载）
    detail = response.xpath("//div[@class='detail-common-text clearfix']/@data-from")
    # 获取json数据链接
    if detail:
        detail_url = 'https:' + detail[0]
        resp = requests.get(detail_url)
        data = resp.text

        data = str(data).replace("var desc='", "").replace("';", '')
        # df = pd.read_html(url,index_col='Year',header=0,parse_dates=True)[0]
        # pandas读取html页面信息
        if "table" in data:
            table = pd.read_html(data)[0]
            # print(table)
            # df_temp = pd.DataFrame(table)
            df_temp = table.astype(object).where(pd.notnull(table), None)
            if len(df_temp) < 5:
                df = df_temp.stack().unstack(0)
            else:
                df = df_temp
            # print(df_temp)
            try:
                item = {"legal_remark1":'',"legal_remark2":''}

                for i in range(len(df)):
                    col = df.iloc[i,0]
                    # print(df.iloc[i,0])

                    if '权利限制情况' in col:
                        # global item
                        lr = df.iloc[i, 1]
                        item["legal_remark1"] = lr if lr else ''
                    if "抵押" in col:
                        ls = df.iloc[i, 1]
                        item["legal_remark2"] = ls if ls else ''

            except Exception as e:
                print("error", e)
                return ''
            else:
                return item
        else:
            return ''
@retry(stop_max_attempt_number=3)
def get_rep_url(url):
    res = requests.get(url,timeout=3)
    # print(res)
    # response = etree.HTML(res.text)
    data = res.text
    # data = json.loads(res.text)
    # print(data)
    data_pattern = re.compile('null\((.*?)\);', re.S)
    result = re.search(data_pattern, data)
    json_list = result.group(1)
    js = json.loads(json_list)
    # print(type(js))
    if not js:
        return ''
    list1 = []
    for data in js:
        id = data["id"]
        # print(id)
        rep_url = "https://sf.taobao.com/download_attach.do?attach_id=" + id
        list1.append(rep_url)
    
    return str(list1)


def get_table():
    conn = pymysql.connect(#host='localhost',
        host='192.168.11.251',
        port=3306,
        user='root',
        password='youtong123',
        # password='mysql',
        database='sipai',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构
    # conn = pymysql.connect(host='www.npacn.com',
    #                             port=3306,
    #                             user='zxlh',
    #                             password='8dMPjf1jIW8c',
    #                             database='sipa_customer',
    #                             charset='utf8',
    #                             cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cur1:
    # sql1 = "SELECT id,title from land_sum_info a WHERE a.confidence is not Null;"
        sql1 = "SELECT id,item_id,itemUrl from new_last_status where id>14412;"
        cur1.execute(sql1)
        # 设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        # 获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        # item = {}
        for result in results:
        # 获取字典中的字段信息
            item_id = result["item_id"]
            item_url = result["itemUrl"]
            id = result["id"]
            #https://sf.taobao.com/json/get_gov_attach.htm?id=569904011480
            data_url = 'https://sf.taobao.com/json/get_gov_attach.htm?id=' + item_id
            report_url = get_rep_url(data_url)

            print(report_url)
            if report_url:
                with conn.cursor() as cur2:
                    sql2 = "update new_last_status set report_url=%s where id = %s"
                    # sql2 = "update 001_house_sum_info set house_type= %s,bd=%s,doc=%s where id = %s"
                    cur2.execute(sql2, (report_url, id))
                    print(id, report_url)
                    print("---" * 50)
                    # print(item_url)
                    conn.commit()
            try:
                item = parse_table(item_url)

            except Exception as e:
                print("error",e)
                pass
            else:
                if item:
                    try:
                        legal_remark1 = item.get("legal_remark1")
                        legal_remark2 = item.get("legal_remark2")
                        legal_remark = legal_remark1 + legal_remark2

                    except Exception:
                        print("error","item不是一个字典")
                        print(id,item_url)
                    else:

                        with conn.cursor() as cur3:
                            sql3 = "update new_last_status set legal_remark=%s where id = %s"
                            # sql2 = "update 001_house_sum_info set house_type= %s,bd=%s,doc=%s where id = %s"
                            cur3.execute(sql3, (legal_remark,id))
                            print(id, legal_remark)
                            # print(item_url)
                            conn.commit()
                            conn.cursor().close()
                            print("**" * 50)

# 多线程，为了提高效率
def multi():
    pool = ThreadPool(processes=8)
    pool.apply_async(get_table, ())
    pool.close()
    pool.join()



if __name__ == '__main__':
    starttime = datetime.datetime.now()
    # multi()
    get_table()
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print("共耗时%s秒" % (time))

# -*- coding: utf-8 -*-
