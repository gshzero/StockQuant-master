import sys

from source.atock_trend_count import atockTrendCount
from source.UsingMysql import UsingMysql
from source.excle_create import ExcelWrite
from source.HttpConnet import HttpConnet
from source.html_date_get import HtmlDataGet
from source.concept_date import Concept
from DB_thread import DB_threading
from globalvar import Global_Data
from http_threading import Http_Threading

import time


class main:
    def getAtockCount(self, days):
        print('-------Get Atock Count start-------')
        with UsingMysql(log_time=True) as um:
            sql = "select stock_number,name,klines from stock_klines"
            data = um.fetch_all(sql, None)
            atock_count = atockTrendCount(data, days)
            atock_count_list = atock_count.get_count()
            table = ExcelWrite('Atock_Count', atock_count_list)
            table.write_sheet()
            table.save_book()

    def update_kline(self, stock_date_list):
        """
        数据层更新数据库日交易数据
        """
        start_time = time.time()
        sql_list = []
        for dict in stock_date_list:
            with UsingMysql(log_time=True) as um:
                sql = "select id  from stock_klines where stock_number = %s " % (dict['code'])
                id = um.get_count(sql, None, 'id')
                print("-- 当前id: %s" % id)
                if id == 0:
                    sql = "INSERT INTO stock_klines ( stock_number, name,klines,week_klines) VALUES ( %s, %s,%s,%s,%s);" % (
                        "\"" + dict['code'] + "\"", "\'" + dict['name'] + "\'", "\"" + str(dict['klines']) + "\"",
                        "\"" + str(dict['week_klines']) + "\"","\"" + str(dict['moon_klines']) + "\"")
                    sql_list.append(sql)
                    print('install success')
                else:
                    sql = "UPDATE stock_klines SET klines=(%s),week_klines=(%s),moon_klines=(%s),name=('%s') WHERE id=('%s')" % (
                    "\"" + str(dict['klines']) + "\"", "\"" + str(dict['week_klines']) + "\"", "\"" + str(dict['moon_klines']) + "\"", str(dict['name']),
                    str(id))
                    sql_list.append(sql)
                    print('update success')
        if len(sql_list) > 0:
            thread_list = []
            N = 0
            for i in sql_list:
                N = N + 1
                thread_list.append(DB_threading(N, i))
                if len(thread_list) >= 50:
                    print("线程数量为", len(thread_list))
                    for thread in thread_list:
                        thread.start()

                    for thread in thread_list:
                        thread.join()  # 10个线程都等待执行完,也就是说,10个线程有一个线程没运行完就不能往下执行代码; 这里会阻塞后面的thread_list=[]和print。但是多个线程间的join和join不会阻塞，也就是说执行完一个join还可以马上执行下一个join，但是执行完最后一个join不能马上执行 thread_list=[]

                    thread_list = []  # 当所有线程运行完清空线程池
                elif len(sql_list) - N < 100:
                    print("线程数量为", len(thread_list))
                    for thread in thread_list:
                        thread.start()

                    for thread in thread_list:
                        thread.join()  # 10个线程都等待执行完,也就是说,10个线程有一个线程没运行完就不能往下执行代码; 这里会阻塞后面的thread_list=[]和print。但是多个线程间的join和join不会阻塞，也就是说执行完一个join还可以马上执行下一个join，但是执行完最后一个join不能马上执行 thread_list=[]

                    thread_list = []  # 当所有线程运行完清空线程池
        print('all stock update success')
        print("总共用时:" + str(time.time() - start_time))

    def update_stock_kline(self):
        """
        业务层更新股票日交易数据
        """
        thread_list = []
        http_connect = HttpConnet()
        global_stock_data = Global_Data()
        # 获取股票列表
        stock_dict = http_connect.get_stock_list()
        stock_dict_longth = len(stock_dict)
        n = 0
        for i in stock_dict:
            thread_list.append(Http_Threading(global_stock_data, i))
            n = n + 1
            if len(thread_list) >= 40:  # 当列表中的线程有10个,就开始执行10个线程
                print("线程数量为", len(thread_list))
                for thread in thread_list:
                    thread.start()
                for thread in thread_list:
                    thread.join()  # 10个线程都等待执行完,也就是说,10个线程有一个线程没运行完就不能往下执行代码; 这里会阻塞后面的thread_list=[]和print。但是多个线程间的join和join不会阻塞，也就是说执行完一个join还可以马上执行下一个join，但是执行完最后一个join不能马上执行 thread_list=[]
                thread_list = []  # 当所有线程运行完清空线程池
            if (len(thread_list) > 0) and (len(stock_dict) - n < 20):
                print("线程数量为", len(thread_list))
                for thread in thread_list:
                    thread.start()
                for thread in thread_list:
                    thread.join()  # 10个线程都等待执行完,也就是说,10个线程有一个线程没运行完就不能往下执行代码; 这里会阻塞后面的thread_list=[]和print。但是多个线程间的join和join不会阻塞，也就是说执行完一个join还可以马上执行下一个join，但是执行完最后一个join不能马上执行 thread_list=[]
                thread_list = []  # 当所有线程运行完清空线程池
            print('progress rate:%d' % (n / stock_dict_longth * 100))
        if len(global_stock_data.get_stock_klines_list()) > 0:
            self.update_kline(global_stock_data.get_stock_klines_list())
        else:
            print("not can get data")

    def updata_stock_message(self):
        """
        更新数据库中股票概念、行业、地区信息
        """
        print('-----update stock message start-----')
        with UsingMysql(log_time=True) as um:
            sql = "select id,stock_number from stock_list"
            id_list = um.fetch_all(sql, None, )
            all_length = len(id_list)
            Serial_number = 0
            if all_length == 0:
                print('not find id of atock' + sql)
                sys.exit(1)
            else:
                stock_concept_list = HtmlDataGet().get_stock_concept(id_list)
                for concept in stock_concept_list:
                    sql = "update stock_list set concept = '%s',Market_value_rank = '%s',profit_rank = '%s', nterprise_sum = '%s'  where id= '%s';" % (
                    concept['concept'], concept['Market_value_rank'], concept['profit_rank'], concept['nterprise_sum'],
                    concept["id"])
                    um.update_by_pk(sql, None)
                    serial_number = Serial_number + 1
                    print(serial_number / len(id_list) * 100)
            print('-----all stock updated-----')

    def get_atock_margin(self, days):
        print('-------get atock margin start-------')
        with UsingMysql(log_time=True) as um2:
            sql = "select a.stock_number,a.name,a.klines,b.concept,b.Market_value_rank,b.profit_rank,b.nterprise_sum from stock_klines a LEFT JOIN stock_list b ON a.stock_number = b.stock_number WHERE (a.stock_number LIKE '000*' OR a.stock_number LIKE '600%' or a.stock_number LIKE '601%' or a.stock_number LIKE '603%' or a.stock_number LIKE '002%') and a.name like '%%'"
            data = um2.fetch_all(sql, None)
            atock_count = atockTrendCount(data, days)
            atock_count_list = atock_count.get_price_margin()
            table = ExcelWrite('margin', atock_count_list)
            table.write_sheet()
            table.save_book()

    def get_atock_bottom(self, days):
        print('-------get atock bottom start-------')
        with UsingMysql(log_time=True) as um2:
            sql = "select a.stock_number,a.name,a.klines,a.moon_klines,b.concept from stock_klines a LEFT JOIN stock_list b ON a.stock_number = b.stock_number WHERE (a.stock_number LIKE '000*' OR a.stock_number LIKE '600%' or a.stock_number LIKE '601%' or a.stock_number LIKE '603%' or a.stock_number LIKE '002%') and a.name NOT like '%ST%'"
            data = um2.fetch_all(sql, None)
            atock_count = atockTrendCount(data, days)
            atock_count_list = atock_count.get_stock_doji()
            table = ExcelWrite('_atock_Doji', atock_count_list)
            table.write_sheet()
            table.save_book()

    def update_tonghuashun_concept_kline(self):
        """
        业务层更新概念日交易数据
        """
        http_connect = Concept()
        # 获取概念列表
        plate_list = http_connect.get_concept_list()
        plate_klines_list = http_connect.get_concept_klines(plate_list)
        if tonghuashun_ is not None:
            with UsingMysql(log_time=True) as um:
                um.delete('delete from tonghuashun_concept')
                for i in plate_klines_list:
                    sql = "select id  from concept_klines where concept_number = '%s'" % (i['concept_number'])
                    id = um.get_count(sql, None, 'id')
                    print("-- 当前id: %s" % id)
                    if id == 0:
                        sql = "INSERT INTO concept_klines ( concept_number, concept_name,klines ) VALUES ( %s, %s,%s);" % (
                            "\"" + i['concept_number'] + "\"", "\'" + i['概念名称'] + "\'", "\"" + i['klines'] + "\"")
                        um.install_one(sql, None)
                        print('install success')
                    else:
                        print(id)
                        sql = "UPDATE concept_klines SET klines=%s WHERE id=%d" % ("\"" + i['klines'] + "\"", id)
                        um.update_by_pk(sql)
                        print('update success')
        else:
            print("concept_klines_list is null")
        print('all concept update success')

    def update_concept_kline(self):
        """
        业务层更新概念日交易数据
        """
        http_connect = Concept()
        # 获取概念列表
        plate_list = http_connect.get_concept_list()
        plate_klines_list = http_connect.get_concept_klines(plate_list)
        if plate_klines_list is not None:
            with UsingMysql(log_time=True) as um:
                um.delete('delete from concept_klines')
                for i in plate_klines_list:
                    sql = "select id  from concept_klines where concept_number = '%s'" % (i['concept_number'])
                    id = um.get_count(sql, None, 'id')
                    print("-- 当前id: %s" % id)
                    if id == 0:
                        sql = "INSERT INTO concept_klines ( concept_number, concept_name,klines ) VALUES ( %s, %s,%s);" % (
                            "\"" + i['concept_number'] + "\"", "\'" + i['概念名称'] + "\'", "\"" + i['klines'] + "\"")
                        um.install_one(sql, None)
                        print('install success')
                    else:
                        print(id)
                        sql = "UPDATE concept_klines SET klines=%s WHERE id=%d" % ("\"" + i['klines'] + "\"", id)
                        um.update_by_pk(sql)
                        print('update success')
        else:
            print("concept_klines_list is null")
        print('all concept update success')

    def get_concept_bottom(self, days):
        print('-------get concept bottom start-------')
        with UsingMysql(log_time=True) as um2:
            sql = "select concept_number,concept_name,klines from concept_klines"
            data = um2.fetch_all(sql, None)
            concept_count = Concept()
            concept_count_list = concept_count.get_concept_doji(data, days)
            table = ExcelWrite('_concept_Doji', concept_count_list)
            table.write_sheet()
            table.save_book()

    def get_rise_concept_list(self, days):
        print('-------get concept bottom start-------')
        with UsingMysql(log_time=True) as um2:
            sql = "select concept_number,concept_name,klines from concept_klines"
            data = um2.fetch_all(sql, None)
            concept_count = Concept()
            concept_count_list = concept_count.get_rise_concep(data, days)
            table = ExcelWrite('_rise_concept_list', concept_count_list)
            table.write_sheet()
            table.save_book()

    def get_atock_rise(self, days):
        print('-------get atock rise list start-------')
        with UsingMysql(log_time=True) as um3:
            sql = "select a.stock_number,a.name,a.klines,b.concept,b.Market_value_rank,b.profit_rank,b.nterprise_sum from stock_klines a LEFT JOIN stock_list b ON a.stock_number = b.stock_number WHERE (a.stock_number LIKE '000%' OR a.stock_number LIKE '600%' or a.stock_number LIKE '601%' or a.stock_number LIKE '603%' or a.stock_number LIKE '605%' or a.stock_number LIKE '002%' or a.stock_number LIKE '689%')  and a.name NOT like '%ST%'"
            data = um3.fetch_all(sql, None)
            atock_count = atockTrendCount(data, days)
            atock_count_list = atock_count.get_rise_stock()
            table = ExcelWrite('_atock_rise', atock_count_list)
            table.write_sheet()
            table.save_book()

    def get_atock_breakthrough(self, days):
        print('-------get atock atock_breakthrough list start-------')
        with UsingMysql(log_time=True) as um3:
            sql = "select a.stock_number,a.name,a.klines,b.concept,b.Market_value_rank,b.profit_rank,b.nterprise_sum from stock_klines a INNER JOIN stock_list b ON a.stock_number = b.stock_number WHERE (a.stock_number LIKE '000%' OR a.stock_number LIKE '600%' or a.stock_number LIKE '601%' or a.stock_number LIKE '603%' or a.stock_number LIKE '605%' or a.stock_number LIKE '002%' or a.stock_number LIKE '689%') AND (a. NAME NOT LIKE '%ST%')"
            data = um3.fetch_all(sql, None)
            atock_count = atockTrendCount(data, days)
            atock_count_list = atock_count.get_breakthrough_stock()
            table = ExcelWrite('_breakthrough', atock_count_list)
            table.write_sheet()
            table.save_book()

    def get_atock_week_breakthrough(self, days):
        print('-------get atock atock_breakthrough list start-------')
        with UsingMysql(log_time=True) as um3:
            sql = "select a.stock_number,a.name,a.klines,a.week_klines,b.concept,b.Market_value_rank,b.profit_rank,b.nterprise_sum from stock_klines a INNER JOIN stock_list b ON a.stock_number = b.stock_number WHERE (a.stock_number LIKE '000%' OR a.stock_number LIKE '600%' or a.stock_number LIKE '601%' or a.stock_number LIKE '603%' or a.stock_number LIKE '605%' or a.stock_number LIKE '002%' or a.stock_number LIKE '689%') AND (a. NAME NOT LIKE '%ST%')"
            data = um3.fetch_all(sql, None)
            atock_count = atockTrendCount(data, days)
            atock_count_list = atock_count.get_week_breakthrough_stock()
            table = ExcelWrite('_week_breakthrough', atock_count_list)
            table.write_sheet()
            table.save_book()

    def get_atock_moon_breakthrough(self, days):
        print('-------get atock——moon__breakthrough list start-------')
        with UsingMysql(log_time=True) as um3:
            sql = "select a.stock_number,a.name,a.klines,a.week_klines,a.moon_klines,b.concept,b.Market_value_rank,b.profit_rank,b.nterprise_sum from stock_klines a INNER JOIN stock_list b ON a.stock_number = b.stock_number WHERE (a.stock_number LIKE '000%' OR a.stock_number LIKE '600%' or a.stock_number LIKE '601%' or a.stock_number LIKE '603%' or a.stock_number LIKE '605%' or a.stock_number LIKE '002%' or a.stock_number LIKE '689%') AND (a. NAME NOT LIKE '%ST%')"
            data = um3.fetch_all(sql, None)
            atock_count = atockTrendCount(data, days)
            atock_count_list = atock_count.get_moon_breakthrough_stock()
            table = ExcelWrite('_moon_breakthrough', atock_count_list)
            table.write_sheet()
            table.save_book()

    def get_week_atock_bottom(self, days):
        print('-------get atock bottom start-------')
        with UsingMysql(log_time=True) as um2:
            sql = "select a.stock_number,a.name,a.week_klines,b.concept from stock_klines a LEFT JOIN stock_list b ON a.stock_number = b.stock_number WHERE (a.stock_number LIKE '000*' OR a.stock_number LIKE '600%' or a.stock_number LIKE '601%' or a.stock_number LIKE '603%' or a.stock_number LIKE '002%') and a.name NOT like '%ST%'  and a.name NOT like '%ST%'"
            data = um2.fetch_all(sql, None)
            atock_count = atockTrendCount(data, days)
            atock_count_list = atock_count.get_week_stock_doji()
            table = ExcelWrite('_week_atock_Doji', atock_count_list)
            table.write_sheet()
            table.save_book()


if __name__ == '__main__':
    # 获取股票最近几天的支撑和案例对比数据
    # main().getAtockCount(5)
    # 更新数据库股票日交易数据
    # main().update_stock_kline()
    # 更新股票概念信息
    # Cookies = 'cid=9694472d4d82cd29fe1c071b36d4d3181627980027; ComputerID=9694472d4d82cd29fe1c071b36d4d3181627980027; WafStatus=0; other_uid=Ths_iwencai_Xuangu_bgee9foa6zwk1ksuqxbxbxdhwp5f26th; ta_random_userid=xgwoi1enwi; vvvv=1; PHPSESSID=9694472d4d82cd29fe1c071b36d4d318; v=A4cFB7L6qhelcC6bSVmvoZBJFjBSjFtutWDf4ll0o5Y9yKkmYVzrvsUwb3xq; '
    # main().updata_stock_message()
    # 获取最近一天缩量下跌股票列表
    # main().get_atock_margin(3)
    # 获取十字星股票列表
    main().get_atock_bottom(5)
    # 更新板块k线记录
    # main().update_concept_kline()
    # 获取上涨趋势概念列表
    # main().get_concept_bottom(5)
    # 统计最近几天上涨的概念
    # main().get_rise_concept_list(5)
    # main().get_atock_rise(3)
    # main().get_atock_breakthrough(5)
    # main().get_atock_week_breakthrough(5)
    # main().get_week_atock_bottom(5)
    # main().get_atock_moon_breakthrough(5)


