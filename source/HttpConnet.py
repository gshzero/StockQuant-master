import requests
import ast
import json

from source.UsingMysql import UsingMysql
from source.excle import ExcelWrite


class HttpConnet(object):
    def get_stock_list(self):
        """调用东方财富接口查询本日交易数据
        return：本日股票交易列表
        """
        stock_today_list = []
        for i in range(1, 230):
            payload = {
                "cb": "jQuery112409772849711893803_1623574203242",
                "pn": i,
                "pz": 20,
                "po": 1,
                "np": 1,
                "ut": "bd1d9ddb04089700cf9c27f6f7426281",
                "fltt": 2,
                "invt": 2,
                "fid": "f3",
                "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",
                "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
                "_": 1623574203489
            }
            r = requests.get(url="https://60.push2.eastmoney.com/api/qt/clist/get", params=payload)
            stock_list_str = str(r.text).partition('(')[2].partition(')')[0]
            stock_list_dict = ast.literal_eval(stock_list_str)
            if len(stock_list_dict['data']['diff']) == 0:
                print('此次获取的列表为空')
            else:
                print('成功获取' + str(i) + '页数据')
                stock_today_list = stock_today_list + stock_list_dict['data']['diff']
        return stock_today_list

    def get_stock_klines(self, stock_number):
        """调用东方财富接口查询历史交易数据
               return：本日股票交易列表
               """
        if stock_number.find('300', 0, 3) > -1 or stock_number.find('301', 0, 3) > -1 or stock_number.find('00', 0, 2) > -1:
            secid = float('0.' + str(stock_number))
        else:
            secid = float('1.' + str(stock_number))
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
