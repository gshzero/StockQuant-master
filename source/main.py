import sys

from source.atock_trend_count import atockTrendCount
from source.UsingMysql import UsingMysql
from source.excle_create import ExcelWrite
from source.HttpConnet import HttpConnet
from source.html_date_get import HtmlDataGet
from source.concept_date import Concept


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

    def update_kline(self, dict):
        """
        数据层更新数据库日交易数据
        """
        stock_klines_tupple = []
        with UsingMysql(log_time=True) as um:
            sql = "select id  from stock_klines where stock_number = %s " % (dict['code'])
            id = um.get_count(sql, None, 'id')
            print("-- 当前id: %s" % id)
            if id == 0:
                sql = "INSERT INTO stock_klines ( stock_number, name,klines ) VALUES ( %s, %s,%s);" % (
                "\"" + dict['code'] + "\"", "\'" + dict['name'] + "\'", "\"" + str(dict['klines']) + "\"")
                um.install_one(sql, None)
                print('install success')
            else:
                stock_klines_tupple.append((str(dict['klines']), str(id)))
            sql = "UPDATE stock_klines SET klines=(%s) WHERE id=(%s)"
            um.update_many(sql, stock_klines_tupple)
            print('update success')

    def update_stock_kline(self):
        """
        业务层更新股票日交易数据
        """
        http_connect = HttpConnet()
        # 获取股票列表
        stock_dict = http_connect.get_stock_list()
        stock_dict_longth = len(stock_dict)
        n = 1
        for i in stock_dict:
            stock_date = http_connect.get_stock_klines(i['f12'])
            print('progress rate:%d' % (n / stock_dict_longth * 100))
            n = n + 1
            if stock_date is not None:
                self.update_kline(stock_date)
            else:
                print("not can get data:" + i['f12'])

        print('all stock update success')

    def updata_stock_message(self, cookies):
        """
        更新数据库中股票概念、行业、地区信息
        """
        print('-----update stock message start-----')
        with UsingMysql(log_time=True) as um:
            sql = "select id,stock_number from stock_list WHERE product = ',房地产,商品房,住宅地产,房地产业务,铁矿'"
            id_list = um.fetch_all(sql, None,)
            all_length = len(id_list)
            Serial_number = 0
            if all_length == 0:
                print('not find id of atock' + sql)
                sys.exit(1)
            for stock_id in id_list:
                # time.sleep(10)
                stock_message = HtmlDataGet(stock_id["stock_number"], cookie=cookies)
                stock_product = stock_message.get_product_list_element()
                stock_concept = stock_message.get_concept_list_element()
                stock_city = stock_message.get_city_element()
                stock_ndustry = stock_message.get_ndustry_element()
                sql = "update stock_list set product = '%s',concept = '%s',city = '%s',ndustry = '%s' where id= '%s';" % (stock_product, stock_concept, stock_city, stock_ndustry, stock_id["id"])
                um.update_by_pk(sql, None)
                serial_number = Serial_number + 1
            print('-----all stock updated-----')

    def get_atock_margin(self, days):
        print('-------get atock margin start-------')
        with UsingMysql(log_time=True) as um2:
            sql = "select a.stock_number,a.name,a.klines,b.concept from stock_klines a LEFT JOIN stock_list b ON a.stock_number = b.stock_number WHERE a.stock_number LIKE '000*' OR a.stock_number LIKE '600%' or a.stock_number LIKE '601%' or a.stock_number LIKE '603%'"
            data = um2.fetch_all(sql, None)
            atock_count = atockTrendCount(data, days)
            atock_count_list = atock_count.get_price_margin()
            table = ExcelWrite('margin', atock_count_list)
            table.write_sheet()
            table.save_book()

    def get_atock_bottom(self, days):
        print('-------get atock bottom start-------')
        with UsingMysql(log_time=True) as um2:
            sql = "select a.stock_number,a.name,a.klines,b.concept from stock_klines a LEFT JOIN stock_list b ON a.stock_number = b.stock_number WHERE a.stock_number LIKE '000*' OR a.stock_number LIKE '600%' or a.stock_number LIKE '601%' or a.stock_number LIKE '603%'"
            data = um2.fetch_all(sql, None)
            atock_count = atockTrendCount(data, days)
            atock_count_list = atock_count.get_stock_doji()
            table = ExcelWrite('_atock_Doji', atock_count_list)
            table.write_sheet()
            table.save_book()

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

if __name__ == '__main__':
    # 获取股票最近几天的支撑和案例对比数据
    # main().getAtockCount(5)
    #更新数据库股票日交易数据
    # main().update_stock_kline()
    #更新股票概念信息
    # Cookies = 'cid=9694472d4d82cd29fe1c071b36d4d3181627980027; ComputerID=9694472d4d82cd29fe1c071b36d4d3181627980027; WafStatus=0; other_uid=Ths_iwencai_Xuangu_bgee9foa6zwk1ksuqxbxbxdhwp5f26th; ta_random_userid=xgwoi1enwi; vvvv=1; PHPSESSID=9694472d4d82cd29fe1c071b36d4d318; v=A4cFB7L6qhelcC6bSVmvoZBJFjBSjFtutWDf4ll0o5Y9yKkmYVzrvsUwb3xq; '
    # main().updata_stock_message(Cookies)
    # 获取上涨股票列表
    # main().get_atock_margin(4)
    # 获取十字星股票列表
    # main().get_atock_bottom(10)
    # 更新板块k线记录
    # main().update_concept_kline()
      main().get_concept_bottom(5)
