# -*- coding: utf-8 -*-
# item = {"auction_people":'','jdu_doc_number':'','legal_remark':'','house_useage_detail':''}
# if True:
#     item["auction_people"] = '张三'
# print(item)
start_price = '1,120,000'
a = str(int(start_price.replace(',', ''))*1000)
print(a)
