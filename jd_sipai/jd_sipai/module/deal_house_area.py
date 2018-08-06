# -*- coding: utf-8 -*-
import json
import re

"""
    部分title中包含了房屋面积信息，可以先从这里获取部分house_area字段信息，共计4764条信息
"""
"""
    处理detail_desc中关于房屋面积的数据
"""


def get_house_area(str_text):
    if str_text:

        detail_desc = re.sub('\s', '', str_text).replace(',','').replace('：','')
        # print(id,detail_desc)
        #匹配有证/建筑面积和无证／土地面积，先把有证／建筑／土地面积的部分匹配出来
        house_area_has_temp = re.findall(r"建筑面积.*?([0-9]+\.[0-9]{1,2})平方米|建筑面积.*?([0-9]+\.[0-9]{1,2})㎡", detail_desc)
        house_area_has = house_area_has_temp if house_area_has_temp else None
        land_area_has_temp = re.findall(r"使用权面积[\u4e00-\u9fa5]?([0-9]+\.[0-9]{1,2})平方米|使用权面积[\u4e00-\u9fa5]?([0-9]+\.[0-9]{1,2})㎡", detail_desc)
        land_area_has = land_area_has_temp if land_area_has_temp else None

        #由于建筑面积提取的结果中由部分重复的数据，需要将列表结果去重
        if house_area_has :
            house_area_has_set = list(set(house_area_has))
            house_area_str = [''.join(house_area) for house_area in house_area_has_set]
            house_area_num = [float(house_area_float) for house_area_float in house_area_str]
            house_area_sum = round(sum(house_area_num),2)
        else:
            house_area_sum = ''
        # print(id,house_area_has_set,house_area_sum)

        if land_area_has:
            land_area_has_set = list(set(land_area_has))
            land_area_str = [''.join(land_area) for land_area in land_area_has_set]
            land_area_num = [float(land_area_float) for land_area_float in land_area_str]
            land_area_sum = round(sum(land_area_num),2)
            # print(id,land_area_has_set,land_area_sum)
        else:
            land_area_sum = ''
        return str(house_area_sum),str(land_area_sum)
    else:
        return None