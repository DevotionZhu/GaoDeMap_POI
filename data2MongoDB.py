# -*- coding:utf-8 -*-
# 将格式化数据导入到mongoDB！
# Written by Mr Wang, Email:1044625113@qq.com
import pymongo


def data2mongo(xlsPath):
    """
    :param xlsPath: excel格式化数据路径
    :return: 返回值为1代表入库成功
    """
    client = pymongo.MongoClient()  # 默认连接本地数据库
    # 根据excel文件名, 创建mongoDB数据库


    # 将excel数据依次导入到mongoDB

    # 建立空间索引


if __name__ == "__main__":
    xlsPath = "北京市_学校.xls"
    data2mongo(xlsPath)

    # client = pymongo.MongoClient()
    # newDB = client['wzp_testDB']
    # newCollection = newDB['dataCollection']
    # dic = {'testName': 'wangzhipan', "id": 1044625113}
    # newCollection.insert_one(dic)
