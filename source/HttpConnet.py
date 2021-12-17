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
        for i in range(1, 238):
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

    def get_stock_rank(self, stock_number):
        """调用东方财富接口查询历史交易数据
               return：本日股票交易列表
               """
        if stock_number.find('300', 0, 3) > -1 or stock_number.find('301', 0, 3) > -1 or stock_number.find('00', 0, 2) > -1:
            secid = float('0.' + str(stock_number))
        else:
            secid = float('1.' + str(stock_number))
        payload = {
            "spt": 1,
            "np": 3,
            "fltt": 2,
            "invt": 2,
            "fields": "f9,f12,f13,f14,f20,f23,f37,f45,f49,f134,f135,f129,f1000,f2000,f3000",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "secid": secid,
            "cb": "jQuery112409803034742232057_1632792905231",
            "_": 1632792905232
        }
        r = requests.get(url="http://push2.eastmoney.com/api/qt/slist/get", params=payload)
        stock_list_str = str(r.text).partition('(')[2].partition(')')[0]
        stock_list_dict = json.loads(stock_list_str)
        if stock_list_dict['data'] is None:
            print('此次获取的列表为空：' + str(secid))
        else:
            market_value = stock_list_dict['data']["diff"][0]["f20"]
            market_rank = stock_list_dict['data']["diff"][0]["f1020"]
            profit_rank = stock_list_dict['data']["diff"][0]["f1045"]
            enterprise_total = stock_list_dict['data']["diff"][1]["f134"]
            market_dict = {"market_value": market_value, "market_rank": market_rank, "profit_rank": profit_rank, "enterprise_total": enterprise_total}

            return market_dict

    def get_stock_klines(self, stock_number):
        """调用东方财富接口查询历史交易数据
               return：本日股票交易列表
               """
        if stock_number.find('300', 0, 3) > -1 or stock_number.find('301', 0, 3) > -1 or stock_number.find('00', 0,
                                                                                                           2) > -1:
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
            print('成功获取' + stock_list_dict['data']["name"] + '日数据')
            #获取月交易数据
        payload3 = {
            "cb": "jQuery112409140191410382024_1638701798116",
            "ut": 'fa5fd1943c7b386f172d6893dbfba10b',
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "fields1": "f1,f2,f3,f4,f5,f6",
            "smplmt": "460",
            "ut": "460",
            "end": 20500101,
            "_": 1638701798138,
            "klt": 103,
            "lmt": 1000000,
            "secid": secid,
            "beg": 0,
            "fqt": 0
        }
        moon_r = requests.get(url="http://43.push2his.eastmoney.com/api/qt/stock/kline/get", params=payload3)
        moon_stock_list_str = str(moon_r.text).partition('(')[2].partition(')')[0]
        moon_stock_list_dict = json.loads(moon_stock_list_str)
        if moon_stock_list_dict['data'] is None:
            print('此次获取的列表为空：' + str(secid))
        else:
            print('成功获取' + moon_stock_list_dict['data']["name"] + '月数据')
            stock_list_dict['data'].update({"moon_klines": moon_stock_list_dict['data']["klines"]})
            # 获取周交易数据
            payload2 = {
                "cb": "jQuery112409656910092235322_1638696481747",
                "fields1": 'f1,f2,f3,f4,f5,f6',
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
                "ut": "fa5fd1943c7b386f172d6893dbfba10b",
                "klt": "102",
                "ut": "fa5fd1943c7b386f172d6893dbfba10b",
                "secid": secid,
                "fqt": 0,
                "end": 20500101,
                "_": 1638696481781,
                "lmt": 120,
                "klt": 102
            }
            week_r = requests.get(url="http://14.push2his.eastmoney.com/api/qt/stock/kline/get", params=payload2)
            week_stock_list_str = str(week_r.text).partition('(')[2].partition(')')[0]
            week_stock_list_dict = json.loads(week_stock_list_str)
            if week_stock_list_dict['data'] is None:
                print('此次获取的列表为空：' + str(secid))
            else:
                print('成功获取' + week_stock_list_dict['data']["name"] + '周数据')
                stock_list_dict['data'].update({"week_klines": week_stock_list_dict['data']["klines"]})
        return stock_list_dict['data']



# book = ExcelWrite('Today_market')
# print(type(stock_list_str))
# print(stock_list_dict['data']['diff'][0]['f14'])
