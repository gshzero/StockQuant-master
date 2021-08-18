import requests
import ast
import json

from source.UsingMysql import UsingMysql
from source.excle import ExcelWrite


class Concept(object):
    def get_concept_list(self):
        """调用东方财富接口查询概念本日交易数据
        return：本日股票交易列表
        """
        plate_list = []
        payload = {
            "cb": "jQuery112308451900112390316_1628866994982",
            "fid": 'f62',
            "po": 1,
            "pz": 50,
            "pn": 1,
            "np": 2,
            "fltt": 2,
            "invt": 2,
            "ut": "b2884a393a59ad64002292a3e90d46a5",
            "fs": "m:90",
            "fields": "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13",
        }
        r = requests.get(url="http://push2.eastmoney.com/api/qt/clist/get", params=payload)
        concept_list_str = str(r.text).partition('(')[2].partition(')')[0]
        concept_list_dict = ast.literal_eval(concept_list_str)
        if len(concept_list_dict['data']['diff']) == 0:
            print('此次获取的列表为空')
        else:
            print('成功获取' +'概念数据列表')
            concept_list = []
            concept_data_list = concept_list_dict['data']['diff'].keys()
            for i in concept_data_list:
                concept_list.append({'概念名称': concept_list_dict['data']['diff'][i]['f14'], '概念代码': concept_list_dict['data']['diff'][i]['f12']})
        return concept_list

    def get_concept_klines(self, concept_list):
        """调用东方财富接口查询概念历史交易K线数据
               return：板块历史交易K线数据列表
               """
        concept_klines_list = []
        payload = {
            "fqt": 0,
            "klt": 101,
            "secid": "",
            "fields1": "f1,f2,f3,f4,f5",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "ut": "fa5fd1943c7b386f172d6893dbfba10b",
            "cb": "jQuery112407817647244615396_1629277494577",
            "_": 1629277494578,
            "beg": 19900101,
            "end": 20220101
        }
        for i in concept_list:
            concept_klines = {}
            payload['secid'] = '90.' + i['概念代码']
            r = requests.get(url="http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get", params=payload)
            concept_list_str = str(r.text).partition('(')[2].partition(')')[0]
            concept_list_dict = json.loads(concept_list_str)
            if concept_list_dict['data'] is None:
                print('此次获取的列表为空：' + i['概念名称'])
            else:
                # print({i['板块名称']: concept_list_dict['data']['klines'], 'palte_number': i['板块代码']})
                concept_klines.update({'概念名称': i['概念名称'], 'klines': str(concept_list_dict['data']['klines']), 'concept_number': i['概念代码']})
                concept_klines_list.append(concept_klines)
        return concept_klines_list


# book = ExcelWrite('Today_market')
# print(type(stock_list_str))
# print(stock_list_dict['data']['diff'][0]['f14'])
