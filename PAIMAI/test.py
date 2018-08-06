# -*- coding: utf-8 -*-
# item = {"auction_people":'','jdu_doc_number':'','legal_remark':'','house_useage_detail':''}
# if True:
#     item["auction_people"] = '张三'
# print(item)

# a= 	["uuid,court,contacts,asset_name,asset_address,longitude,latitude,"
#        "asset_type,asset_no,evaluate_price,starting_price,deal_price,report_no,asset_holders,"
# 	"case_no,trade_date,auction_type,auction_status,legal_remark,asset_des,province,city,source_name,source_url,coordniate"]
# b = '""'.join(a)
# print(b)
from datetime import datetime, timedelta, date

from lxml import etree

import pandas as pd
import requests


# def read_table(url):
#     res = requests.get(url)
#     response = etree.HTML(res.text)
#     # 标的物详情描述,正则匹配（异步加载）
#     detail = response.xpath("//div[@class='detail-common-text clearfix']/@data-from")
#     # 获取json数据链接
#     if detail:
#         detail_url = 'https:' + detail[0]
#         resp = requests.get(detail_url)
#         data = resp.text
#
#         data = str(data).replace("var desc='", "").replace("';", '')
#         # df = pd.read_html(url,index_col='Year',header=0,parse_dates=True)[0]
#         # pandas读取html页面信息
#         if "table" in data:
#             table = pd.read_html(data)[0]
#             # print(table)
#             # df_temp = pd.DataFrame(table)
#             df_temp = table.astype(object).where(pd.notnull(table), None)
#             print(df_temp)
#
# if __name__ == '__main__':
#     url = 'https://sf.taobao.com/sf_item/571119805139.htm'
#     read_table(url)


#两天以前
# today = date.today()
# yes = today - timedelta(days=2)


#先获得时间数组格式的日期
# threeDayAgo = (datetime.now() - datetime.timedelta(days = 3))
#转换为时间戳:
# timeStamp = int(time.mktime(threeDayAgo.timetuple()))
#转换为其他字符串格式:
# strTime = yes.strftime("%Y-%m-%d")
# print(strTime)
# print(today)
# print(yes)
# print(strTime)

str1 = None
str2 = None
str = str1 + ',' + str2
print(str)