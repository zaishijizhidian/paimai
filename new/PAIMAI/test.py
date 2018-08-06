# -*- coding: utf-8 -*-
import json

item = {"auction_people":None,'jdu_doc_number':'张三','legal_remark':'1445','house_useage_detail':None}
# if True:
#     item["auction_people"] = '张三'
# print(item)
start_price = '1,120,000'
a = str(float(start_price.replace(',', ''))*1000)
print(a)
js_data = json.dumps(item,ensure_ascii=False)
print(type(js_data))