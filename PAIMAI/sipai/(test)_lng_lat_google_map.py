# -*- coding: utf-8 -*-
import json

import requests


def get_latlng(addr):
    ak='Ml0kB3WSGGjyIo8V2PznW0wjUo2xWQeH'
    url='http://api.map.baidu.com/geocoder/v2/'
    # url='http://api.map.baidu.com/geocoder'

    payload={
    'output':'json',
    'ak':ak,
    # 'coord_type':'bd09',
    # 'callback':'showLocation',
    'address':addr,
    'src':"经纬度"
    }
    # try:
    response=requests.get(url,params=payload)
    # print response
    contents=response.content.decode('utf-8')
    # print type(content)
    json_result=json.loads(contents)
    # print(eval(contents))
    print(json_result)

    coordinate = json_result["result"]["location"]
    # print(coordinate)
    confidence=json_result['result']['confidence']
    # print(confidence)
    # if confidence >50:
    #     lng = coordinate["lng"]
    #     lat = coordinate["lat"]
    # else:
    #     lng = 0
    #     lat = 0
    lng = coordinate["lng"]
    lat = coordinate["lat"]
    print(lng,lat,confidence)
    return lng,lat


if __name__ == '__main__':
    address = "安徽省宁国市翠竹家园6幢"
    get_latlng(address)
    # 浙江温州泰顺县罗阳镇镇中路的经纬度是: 27.551509, 119.711175