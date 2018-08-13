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

from model.deal_taobao_aution_info import clean_data


def read_table(url):
#     res = requests.get(url)
#     response = etree.HTML(res.text)
#     # 标的物详情描述,正则匹配（异步加载）
#     detail = response.xpath("//div[@class='detail-common-text clearfix']/@data-from")
#     # 获取json数据链接
#     if detail:
#         detail_url = 'https:' + detail[0]
    resp = requests.get(url)
    data = resp.text

    data = str(data).replace("var desc='", "").replace("';", '')
    item = {"auction_people": '', 'jdu_doc_number': '', 'legal_remark': '', 'house_useage_detail': ''}
    # df = pd.read_html(url,index_col='Year',header=0,parse_dates=True)[0]
    # pandas读取html页面信息
    if "table" in data:
        table = pd.read_html(data)[0]
        print(table)

        # df_temp = pd.DataFrame(table)
        df_temp = table.astype(object).where(pd.notnull(table), None)
        if len(df_temp) < 5:
            df = df_temp.stack().unstack(0)
        else:
            df = df_temp
        # print(df_temp)
        try:
            mark = []
            house_useage = []
            for i in range(len(df)):
                col = str(df.iloc[i,0])
                # print(df.iloc[i,0])
                if col == '拍品所有人' or col =='房屋所有权人'or col == '标的所有人' or col == '土地使用权人' or col == '标的物所有权人':
                    bd= str(df.iloc[i,1])
                    if bd:
                        item["auction_people"] = clean_data(bd)
                        # item.update(dict1)
                    else:
                        item["auction_people"] = ''

                elif col == '执行所依据的法律文书' or col =='执行案号' :
                    # dict1 = {}
                    doc = str(df.iloc[i, 1])
                    item["jdu_doc_number"] = doc if doc else ''
                elif col == '法院执行裁定书' :
                    doc = str(df.iloc[i, 2])
                    item["jdu_doc_number"] = doc if doc else ''
                    # item.update(dict1)
                    # print(item["doc"])

                elif  col == '权利限制情况' :
                    doc = str(df.iloc[i, 1])
                    legal_remark1 = doc if doc else ''
                    mark.append(legal_remark1)

                elif col == '抵押':
                    ls = str(df.iloc[i, 1])
                    legal_remark2 = ls if ls else ''
                    mark.append(legal_remark2)

                    # item.update(dict1)
                    # print(item["doc"])
                    # print(i)
                elif col == '房屋用途及土地性质' or col == '用途' or col == '土地用途' :
                    house_type = str(df.iloc[i, 1])
                    # item["house_useage_detail"] = house_type if house_type else ''
                    detail1 = house_type if house_type else ''
                    house_useage.append(detail1)
                    # item.update(dict1)
                elif col == '拍品现状' or col == '标的现状':
                    try:
                        house_type = str(df.iloc[i, 2])
                    except Exception:
                        house_type = str(df.iloc[i, 1])
                    detail2 = house_type if house_type else ''
                    house_useage.append(detail2)
                item['legal_remark'] = ','.join(mark)
                item['house_useage_detail'] = ','.join(house_useage)

        except Exception as e:
            print(e,"error %s" % url)
            print(item)
            return item
        else:
            print(item)
            return item
    else:
        print(item)
        return item

if __name__ == '__main__':
    url = 'https://desc.alicdn.com/i4/570/980/572984730978/TB1Gof1tLiSBuNkSnhJ8qvDcpla.desc%7Cvar%5Edesc%3Bsign%5E557043ea6591e033506c24ae96617256%3Blang%5Egbk%3Bt%5E1532054702'
    read_table(url)


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

# str1 = None
# str2 = None
# str = str1 + ',' + str2
# print(str)