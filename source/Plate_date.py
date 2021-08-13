import requests
import ast
import json

from source.UsingMysql import UsingMysql
from source.excle import ExcelWrite


class Plate(object):
    def get_plate_list(self):
        """调用东方财富接口查询本日交易数据
        return：本日股票交易列表
        """
        plate_list = []
        payload = {
            "cb": "jQuery112308451900112390316_1628866994982",
            "fid": 'f62',
            "po": 1,
            "pz": 50,
            "pn": 1,
            "np": 1,
            "fltt": 2,
            "invt": 2,
            "ut": "b2884a393a59ad64002292a3e90d46a5",
            "fs": "m:90 t:2",
            "fields": "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13",
        }
        r = requests.get(url="http://push2.eastmoney.com/api/qt/clist/get", params=payload)
        plate_list_str = str(r.text).partition('(')[2].partition(')')[0]
        plate_list_dict = ast.literal_eval(plate_list_str)
        if len(plate_list_dict['data']['diff']) == 0:
            print('此次获取的列表为空')
        else:
            print('成功获取' +'板块数据列表')
            for i in plate_list_dict['data']['diff']:
                plate_list = plate_list.append({i['f14']: i['f12']})
        return plate_list

    def get_plate_klines(self, stock_number):
        """调用东方财富接口查询板块历史交易K线数据
               return：板块历史交易K线数据列表
               """
        payload = {
            "cb": "jQuery1124039604947555317227_1623587960569",
            "fields1": 'f1,f2,f3,f4,f5,f6',
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "klt": "101",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "secid": secid,
            "fqt": 1,
            "beg": 0,
            "end": 20500000,
            "_": 1623587960608,
            "lmt": 1000000
        }
        r = requests.get(url="http://push2his.eastmoney.com/api/qt/stock/kline/get", params=payload)
        stock_list_str = str(r.text).partition('(')[2].partition(')')[0]
        stock_list_dict = json.loads(stock_list_str)
        if stock_list_dict['data'] is None:
            print('此次获取的列表为空：' + str(secid))
        else:
            print('成功获取' + stock_list_dict['data']["name"] + '数据')
            return stock_list_dict['data']


# book = ExcelWrite('Today_market')
# print(type(stock_list_str))
# print(stock_list_dict['data']['diff'][0]['f14'])
