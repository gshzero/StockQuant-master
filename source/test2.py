#coding=utf-8import MySQLdb
import traceback

tmp = "insert into exch_no_rand_auto(stkcode) values(%s);"   #SQL模板字符串
l_tupple = [(i,) for i in range(100)]   #生成数据参数，list里嵌套tuple

class mymysql(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='127.0.0.1',
            port = 3306,
            user = 'root',
            passwd = '123456',
            db = 'xtp3')

    def insert_sql(self,temp,data):
        cur = self.conn.cursor()
        try:
            cur.executemany(temp,data)
            self.conn.commit()
        except:
            self.conn.rollback()
            traceback.print_exc()
        finally:
            cur.close()

if __name__ == '__main__':
    m = mymysql()
    m.insert_sql(tmp,l_tupple)