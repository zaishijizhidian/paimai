# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from urllib.request import urlopen
import json

def getAddress(address):

    addressUrl = "http://maps.googleapis.com/maps/api/geocode/json?"
    url = addressUrl + urlencode({ 'address': address})
    print('Retrieving:', url)
    uh = urlopen(url)
    data = uh.read()
    responseJson = json.loads(data.decode('utf-8'))

    lat = responseJson.get('results')[0]['geometry']['location']['lat']
    lng = responseJson.get('results')[0]['geometry']['location']['lng']
    print(address + '的经纬度是: %f, %f' % (lat, lng))
    return [lat, lng]


if __name__ == '__main__':
    address = "浙江温州泰顺县罗阳镇镇中路13-1号"
    getAddress(address)