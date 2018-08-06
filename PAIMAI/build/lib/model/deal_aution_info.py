import re

import pandas as pd

import requests

from retrying import retry
import json

"""
解析拍卖详情的表格数据，提取出拍品所有人，权利限制情况，法律文书，房屋用途等信息

"""
def parse_table(url):
    resp = requests.get(url)
    data = resp.text
    data = str(data).replace("var desc='", "").replace("';", '')
    # df = pd.read_html(url,index_col='Year',header=0,parse_dates=True)[0]
    # pandas读取html页面信息
    item = {"auction_people": '', 'jdu_doc_number': '', 'legal_remark': '', 'house_useage_detail': ''}
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
            mark = []
            house_useage = []
            for i in range(len(df)):
                col = df.iloc[i,0]
                # print(df.iloc[i,0])
                if col == '拍品所有人' or col =='房屋所有权人'or col == '标的所有人' or col == '土地使用权人':
                    bd= df.iloc[i,1]
                    if bd:
                        item["auction_people"] = clean_data(bd)
                        # item.update(dict1)
                    else:
                        item["auction_people"] = ''

                elif col == '执行所依据的法律文书' or col =='执行案号' :
                    # dict1 = {}
                    doc = df.iloc[i, 1]
                    item["jdu_doc_number"] = doc if doc else ''
                elif col == '法院执行裁定书' :
                    doc = df.iloc[i, 2]
                    item["jdu_doc_number"] = doc if doc else ''
                    # item.update(dict1)
                    # print(item["doc"])

                elif  col == '权利限制情况' :
                    doc = df.iloc[i, 1]
                    legal_remark1 = doc if doc else ''
                    mark.append(legal_remark1)

                elif col == '抵押':
                    ls = df.iloc[i, 1]
                    legal_remark2 = ls if ls else ''
                    mark.append(legal_remark2)

                    # item.update(dict1)
                    # print(item["doc"])
                    # print(i)
                elif col == '房屋用途及土地性质' or col == '用途' or col == '土地用途' :
                    house_type = df.iloc[i, 1]
                    # item["house_useage_detail"] = house_type if house_type else ''
                    detail1 = house_type if house_type else ''
                    house_useage.append(detail1)
                    # item.update(dict1)
                elif col == '拍品现状' or col == '标的现状':
                    house_type = df.iloc[i, 2]
                    detail2 = house_type if house_type else ''
                    house_useage.append(detail2)
                item['legal_remark'] = ','.join(mark)
                item['house_useage_detail'] = ','.join(house_useage)

        except Exception as e:
            print("error", e)
            pass
        else:
            return item
    else:
        return item



def clean_data(str):
    strs = str.replace('所有','').replace('权','').replace('共有','').replace('单独','').replace('共同','').replace('。','').replace('被执行','').replace('（','').replace('）','')
    if "人" in strs:
        if ":" in strs :
            st = strs.split(':')[-1]
        elif "：" in strs :
            st = strs.split('：')[-1]
        else:
            st = strs.replace('人','')
        return st

    else:
        return strs


@retry(stop_max_attempt_number=3)
def get_rep_url(url):
    res = requests.get(url, timeout=3)
    # print(res)
    # response = etree.HTML(res.text)
    data = res.text
    # data = json.loads(res.text)
    # print(data)
    data_pattern = re.compile('null\((.*?)\);', re.S)
    result = re.search(data_pattern, data)
    if result:
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

# if __name__ == '__main__':
#     url = 'https://sf.taobao.com/sf_item/570036380942.htm'
#     data_url = 'https://desc.alicdn.com/i1/560/500/567506029769/TB1QbVylASWBuNjSszd8qveSpla.desc%7Cvar%5Edesc%3Bsign%5Eb8a0e3e883cc992cc3b3572a2200e02a%3Blang%5Egbk%3Bt%5E1523515930'
#     # res = requests.get(url)
#     # # print(11)
#     # response = etree.HTML(res.text)
#     # detail = response.xpath("//div[@class='detail-common-text clearfix']/@data-from")[0]
#     # # print(detail)
#     # # 获取json数据链接
#     # detail_url = 'https:' + detail
#
#     # it = parse_table(detail_url)
#     it = parse_table(data_url)
#     print(it)