# -*- coding:utf-8 -*-
# 利用geoIP获取电脑所在经纬度！
# Written by Mr Wang, Email:1044625113@qq.com
import socket

import geoip2.database


def getMyIp():
    """
    :return: 返回IP地址
    """
    # 获取本机电脑名
    myname = socket.getfqdn(socket.gethostname())
    # 获取本机ip
    myaddr = socket.gethostbyname(myname)
    return myaddr


def ip2location(input_ip, GeoCityPath):
    """
    :input_ip IP:  电脑IP地址
    :GeoCityPath: 本地城市数据库
    :return: 返回电脑经纬度
    """

    try:
        reader = geoip2.database.Reader(GeoCityPath)
        data = reader.city(input_ip)

        city = data.city.name
        country = data.country.name
        postal_code = data.postal.code  # 邮编
        longitude = data.location.longitude  # 经度
        latitude = data.location.latitude  # 纬度

        return longitude, latitude, city
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    # Ip = getMyIp()
    Ip = "18.162.147.79"
    GeoCityPath = "IP地址库//GeoLite2-City.mmdb"

    longitude, latitude, city = ip2location(Ip, GeoCityPath)
    print(longitude)
    print(latitude)
    print(city)
