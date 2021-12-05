import requests
import ast
import json
from source.tool import Tool

from source.UsingMysql import UsingMysql
from source.excle import ExcelWrite


class news_finance(object):
    def get_news(self, page):
        """调用新浪财经新闻接口返回最新20条新闻
        return：json格式最新20条新闻
        """
        news_str = ''
        news_word = ['工信部','失业率','进口','感染','疫苗','美联储','就业','天齐',
                                      '锂','美国','欧盟','铁矿','原油','特斯拉','比亚迪','央行',
                                      '住房和城乡建设部','自贸区','商务部','铁路','保监会','新能源',
                                      '乘联会','大湾区','确诊','工业和信息化部','发改委','教育部',
                                      '沪深','苹果','军事','住建部']
        payload = {
            "callback": "jQuery111204006017353852478_1630322898913",
            "page": page,
            "page_size": 20,
            "zhibo_id": 152,
            "tag_id": 0,
            "dire": "f",
            "dpc": 1,
            "pagesize": 1000,
            "_": "1630322898914",
        }
        r = requests.get(url="https://zhibo.sina.com.cn/api/zhibo/feed", params=payload)
        news_list_str = str(r.text).partition('jQuery111204006017353852478_1630322898913(')[2].partition(');}')[0]
        news_list_dict = ast.literal_eval(news_list_str)
        if news_list_dict['result']['status']['msg'] != 'OK':
            print('此次获取的列表为空')
        else:
            news_list = []
            news_data_list = news_list_dict['result']['data']['feed']['list']
            for i in news_data_list:
                for key_word in news_word:
                    if i['rich_text'].find(key_word) >=0:
                        news_str = news_str + i['rich_text'] + '\n' + i['create_time'] + '\n'
        return news_str

if __name__ == '__main__':
    a = news_finance()
    news_str = ''
    for i in range(1, 50):
        news_str = news_str + a.get_news(i)
    data = open("E:\股票\新闻.txt", 'w+')
    print('news_str', file=data)
    data.close()