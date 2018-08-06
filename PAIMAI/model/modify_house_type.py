# -*- coding: utf-8 -*-

"""
用于判断标的物类型
"""


def modify_type(str):
    list1 = ['住宅','住房','房屋','房产','公寓','含车位','别墅','单元','苑','小区','房地产','幢','室']
    list2 = ['办公','写字楼','商办','商务','商住','商务中心','国贸']
    list3 = ['商铺','商服','商网','商贸','商城','市场','商场','营业','商业','门面','门点','铺位','铺面','底商','店铺','门店','门市','酒店','店面']
    list4 = ['车库','车位','地下室','停车场','车房','储藏室']
    list5 = ['土地','使用权','林地','用地','亩']
    list6 = ['建筑物','厂房','工业','附着物','在建工程']
    type = None
    for str2 in list1:
        if str.rfind(str2)>=0:
            type = '01'
    for str2 in list2:
        if str.rfind(str2) >= 0:
            type = '02'
    for str2 in list3:
        if str.rfind(str2) >= 0:
            type = '03'
    for str2 in list4:
        if str.rfind(str2) >= 0:
            type = '04'
    for str2 in list5:
        if str.rfind(str2) >= 0:
            type = '05'
    for str2 in list6:
        if str.rfind(str2) >= 0:
            type = '06'
    if type is None:
        type = '07'
    return type

if __name__ == '__main__':
    str = '伊春区红升办军分区修理所综合楼1号楼2单元7层东厅房产'
    type = modify_type(str)
    print(type)