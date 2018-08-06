# -*- coding: utf-8 -*-
import json
import re



"""
    处理detail_desc中关于房屋面积的数据
"""



def get_house_cardnum(str_text):

    item = {}
    if str_text:
        detail_desc = re.sub('\s', '', str_text).replace(',','')
        # print(id,detail_desc)

        #匹配房屋权证号 贵港房权证贵港市字第10077191号
        house_crefid_temp = re.search(r"[\u4e00-\u9fa5]{1,2}房权证(.*?字第.*?号)",detail_desc)
        if house_crefid_temp:
            item["house_crefid"] = house_crefid_temp.group(0)
        else:
            item["house_crefid"] = None

        #匹配土地权证号
        land_crefid_temp = re.search(r"[\u4e00-\u9fa5]国用(.*?)第(.*?)号",detail_desc)
        if land_crefid_temp:
            item["land_crefid"] = land_crefid_temp.group(0)
        else:
            item["land_crefid"]= None
        # if item["house_crefid"] or item["land_crefid"] :
        js_data = json.dumps(item, ensure_ascii=False)
        return js_data

    else:
        return None
