import requests
import ast
import json
from source.tool import Tool


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
            r = requests.get(url="https://push2his.eastmoney.com/api/qt/stock/kline/get", params=payload)
            concept_list_str = str(r.text).partition('(')[2].partition(')')[0]
            concept_list_dict = json.loads(concept_list_str)
            if concept_list_dict['data'] is None:
                print('此次获取的列表为空：' + i['概念名称'])
            else:
                # print({i['板块名称']: concept_list_dict['data']['klines'], 'palte_number': i['板块代码']})
                concept_klines.update({'概念名称': i['概念名称'], 'klines': str(concept_list_dict['data']['klines']), 'concept_number': i['概念代码']})
                concept_klines_list.append(concept_klines)
                print(payload['secid'])
        return concept_klines_list

    def get_concept_doji(self, date, days,):
        """
        获取最近大概率上涨的股票概念
        date:股票字典列表
        days:统计周期
        """
        concept_price_margin = []
        for concept in date:
            concept_count_dict = {}
            concept_number = concept['concept_number']
            concept_name = concept['concept_name']
            klines = concept['klines'].replace('[', '').replace(']', '').split(', ')
            if len(klines) >= days:
                statistical_period = klines[len(klines) - days:len(klines)]
                statistical_period = Tool().spilt_str_list(statistical_period)
                difference1 = 0
                difference2 = 0
                if (float(statistical_period[len(statistical_period) - 2][8]) < 0) and (
                        float(statistical_period[len(statistical_period) - 1][8]) > 0):
                    a1 = (float(statistical_period[len(statistical_period) - 2][1]) - float(
                        statistical_period[len(statistical_period) - 2][2]))
                    a1 = [a1, 1000000][a1 == 0]
                    difference1 = (float(statistical_period[len(statistical_period) - 2][3]) - float(
                        statistical_period[len(statistical_period) - 2][4])) / a1
                elif (float(statistical_period[len(statistical_period) - 3][8])) < 0 and (
                        float(statistical_period[len(statistical_period) - 1][8]) > 0):
                    a2 = (float(statistical_period[len(statistical_period) - 3][1]) - float(
                        statistical_period[len(statistical_period) - 3][2]))
                    a2 = [a2, 1000000][a2 == 0]
                    difference2 = (float(statistical_period[len(statistical_period) - 3][3]) - float(
                        statistical_period[len(statistical_period) - 3][4])) / a2
                else:
                    continue
                    # 判断最后2天收盘价与开票价盘的差与幅度的比
                if difference1 >= 1 or difference2 >= 1 and (difference1 != 0 and difference2 != 0):
                    turnover_rate1 = float(statistical_period[len(statistical_period) - 2][10])
                    turnover_rate2 = float(statistical_period[len(statistical_period) - 3][10])
                    turnover_rate = [turnover_rate1, turnover_rate2][difference2 >= difference1]
                    rate = turnover_rate
                    for change1 in statistical_period:
                        if float(change1[10]) <= turnover_rate:
                            turnover_rate = float(change1[10])
                        else:
                            continue
                    if turnover_rate >= rate:
                        concept_count_dict.update({'概念代码': concept_number})
                        concept_count_dict.update({'概念名称': concept_name})
                        reciprocal_two = float(statistical_period[len(statistical_period) - 2][8])
                        reciprocal_three = float(statistical_period[len(statistical_period) - 3][8])
                        if reciprocal_two <= reciprocal_three:
                            concept_count_dict.update(
                                {'最近2天最小跌幅': float(statistical_period[len(statistical_period) - 2][8])})
                        else:
                            concept_count_dict.update(
                                {'最近2天最小跌幅': float(statistical_period[len(statistical_period) - 3][8])})
                        concept_price_margin.append(concept_count_dict)
                else:
                    continue
        return concept_price_margin

    def get_rise_concep(self, date, days):
        """
        统计最近连续上涨天数的占比
        date:股票字典列表
        days:统计周期
        """
        concept_price_margin = []
        for concept in date:
            concept_count_dict = {}
            concept_number = concept['concept_number']
            concept_name = concept['concept_name']
            klines = concept['klines'].replace('[', '').replace(']', '').split(', ')
            if len(klines) >= days:
                statistical_period = klines[len(klines) - days:len(klines)]
                statistical_period = Tool().spilt_str_list(statistical_period)
                n = 0
                for i in range(1, days+1):
                    price = float(statistical_period[len(statistical_period) - i][8])
                    if price > 0:
                        n = n + 1
                    else:
                        break
                    if n <= days:
                        price_disparity = (float(statistical_period[len(statistical_period) - 1][2]) - float(statistical_period[len(statistical_period) - days][2]))/float(statistical_period[len(statistical_period) - days][2])*100
                        concept_count_dict.update({'概念代码': concept_number})
                        concept_count_dict.update({'概念名称': concept_name})
                        concept_count_dict.update({'上涨幅度': price_disparity})
                        concept_price_margin.append(concept_count_dict)
        return concept_price_margin

# book = ExcelWrite('Today_market')
# print(type(stock_list_str))
# print(stock_list_dict['data']['diff'][0]['f14'])
