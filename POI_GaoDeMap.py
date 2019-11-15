# coding:utf-8
import json
from urllib import request
from urllib.parse import quote

import math
import xlwt


# 作者:wangzhipan,Email:1044625113@qq.com
# 特别注意,高德地图下载的POI点为火星坐标系统,我们需要后续处理,转成WGS84坐标系统下才能用


# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, i)
        print(result)
        result = json.loads(result)  # 将字符串转换为json
        if result['count'] == '0':
            break
        hand(poilist, result)
        i = i + 1
    return poilist


# 高德地图坐标转WGS84坐标系统
def transformlat(lng, lat):
    pi = 3.1415926535897932384626

    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.002 * math.sqrt(abs(lng))
    ret = ret + (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
                 math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret = ret + (20.0 * math.sin(lat * pi) + 40.0 *
                 math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret = ret + (160.0 * math.sin(lat / 12.0 * pi) + 320 *
                 math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    pi = 3.1415926535897932384626

    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    ret = ret + (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
                 math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret = ret + (20.0 * math.sin(lng * pi) + 40.0 *
                 math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret = ret + (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
                 math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def GD_to_WGS84(lng, lat):
    pi = 3.1415926535897932384626
    ee = 0.00669342162296594323  # 偏心率平方
    a = 6378245.0  # 长半轴

    if lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55:  # 判断是否在中国范围内, 在国内需要进行偏移
        dlat = transformlat(lng - 105.0, lat - 35.0)
        dlng = transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * pi
        magic = math.sin(radlat)
        magic = 1 - ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
        dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
        mglat = lat + dlat
        mglng = lng + dlng
        longitude = lng * 2 - mglng
        latitude = lat * 2 - mglat
    else:
        longitude = lng
        latitude = lat
    return longitude, latitude


# 数据写入excel
def write_to_excel(poilist, cityname, classfield):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(classfield, cell_overwrite_ok=True)

    # 第一行(列标题)
    sheet.write(0, 0, 'longitude')
    sheet.write(0, 1, 'latitude')
    sheet.write(0, 2, 'count')
    sheet.write(0, 3, 'name')
    sheet.write(0, 4, 'address')
    sheet.write(0, 5, 'tel')

    for i in range(len(poilist)):
        location = poilist[i]['location']
        name = poilist[i]['name']
        address = poilist[i]['address']
        tel = poilist[i]['tel']
        lng = str(location).split(",")[0]
        lat = str(location).split(",")[1]
        lng, lat = GD_to_WGS84(float(lng), float(lat))  # 高德地图(火星坐标)转换为WGS84坐标
        lng = str(lng)
        lat = str(lat)

        '''
        result = gcj02_to_wgs84(float(lng), float(lat))

        lng = result[0]
        lat = result[1]
        '''

        # 每一行写入
        sheet.write(i + 1, 0, lng)
        sheet.write(i + 1, 1, lat)
        sheet.write(i + 1, 2, 1)
        sheet.write(i + 1, 3, name)
        sheet.write(i + 1, 4, address)
        sheet.write(i + 1, 5, tel)

    # 最后，将以上操作保存到指定的Excel文件中
    book.save(r'' + cityname + "_" + classfield + '.xls')


# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


# 单页获取pois
def getpoi_page(cityname, keywords, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data


# TODO 替换为上面申请的密钥
amap_web_key = 'your api key'
poi_search_url = "http://restapi.amap.com/v3/place/text"
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"
# from transCoordinateSystem import gcj02_to_wgs84

# TODO cityname为需要爬取的POI所属的城市名，nanning_areas为城市下面的所有区，classes为多个分类名集合. (中文名或者代码都可以，代码详见高德地图的POI分类编码表)
cityname = '北京市'
# nanning_areas = ['望城区', '开福区', '岳麓区', '天心区', '雨花区', '芙蓉区']
nanning_areas = ['东城区', '西城区', '朝阳区', '海淀区']

# classes = ['商场', '超级市场', '综合市场', '运动场馆', '娱乐场所', '影剧院', '医院', '宾馆酒店', '公园广场',
#            '风景名胜', '科研机构', '政府机关', '博物馆', '展览馆', '美术馆', '图书馆',
#            '学校', '火车站', '机场', '港口码头', '会展中心', '停车场', '银行']
classes = ['学校', '医院', '地铁站', '公交站', '公园']

for clas in classes:
    classes_all_pois = []
    for area in nanning_areas:
        pois_area = getpois(area, clas)
        print('当前城区：' + str(area) + ', 分类：' + str(clas) + ", 总的有" + str(len(pois_area)) + "条数据")
        classes_all_pois.extend(pois_area)
    print("所有城区的数据汇总，总数为：" + str(len(classes_all_pois)))

    write_to_excel(classes_all_pois, cityname, clas)

    print('================分类：' + str(clas) + "写入成功")
