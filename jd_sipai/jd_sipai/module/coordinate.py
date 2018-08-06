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
    # print(type(json_result["status"]))

    if json_result["status"] == 0:
        coordinate = json_result["result"]["location"]
        # print(coordinate)
        confidence=json_result['result']['confidence']
        #经度坐标,进度的坐标要比维度的大
        lng = str(coordinate["lng"])
        # 纬度坐标，较小的那个坐标
        lat = str(coordinate["lat"])



    else:

        confidence = ''
        lng = ''
        lat = ''

    return confidence,lat,lng
