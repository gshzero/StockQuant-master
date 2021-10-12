
import os, threading
from DBUtils.PooledDB import PooledDB
import pymysql, random, time


# 创建一个有10个连接的mysql连接池.创建并维持10个线程并发写入1000000条随机数据到test.stu表中

class DB_threading(threading.Thread):
    def __init__(self, n, sql):
        super(DB_threading, self).__init__()
        mysql_conf = {
            "host": "localhost",
            "user": "root",
            "passwd": "13549812386",
            "charset": "utf8",
            "db": "atock",
            "cursorclass": pymysql.cursors.DictCursor
        }

        # 创建一个连接池,连接池初始最多容纳和创建25个连接,当连接池没有可用连接则阻塞
        # 使用连接池可以进行长连接,无需每次操作mysql时都建立连接,节省了建立连接的时间
        self.n = n
        self.pool = PooledDB(pymysql, maxconnections=0, blocking=True, **mysql_conf)
        self.sql = sql
        # self.sex = ["m", "s"]

    def run(self,):
        print("%s号线程开始任务" % self.n)
        sql = self.sql

        # 获取连接
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, None)  # 批量操作,提高效率
            conn.commit()
            print("%s号线程完成任务" % self.n)
        except:
            # 如果出现错误,要回滚
            conn.rollback()
            print("%s号线程任务失败" % self.n)
        finally:
            # 无论插入成功还是失败,记得将连接放回连接池供其他线程使用,否则该线程会一直被占用
            cursor.close()
            conn.close()  # 执行完sql操作后,将连接放回连接池,而不是真的关闭连接.如果不放回连接池,则该连接一直处于占用状态,其他线程就无法使用该连接

    # 最多创建10个线程并发执行


# start_time = time.time()
# thread_list = []  # 创建线程池
# for i in range(500):
#     thread_list.append(DB_threading(i))
#     if len(thread_list) >= 100:  # 当列表中的线程有10个,就开始执行10个线程
#         print("线程数量为", len(thread_list))
#         print(i)
#         for thread in thread_list:
#             thread.start()
#
#         for thread in thread_list:
#             thread.join()  # 10个线程都等待执行完,也就是说,10个线程有一个线程没运行完就不能往下执行代码; 这里会阻塞后面的thread_list=[]和print。但是多个线程间的join和join不会阻塞，也就是说执行完一个join还可以马上执行下一个join，但是执行完最后一个join不能马上执行 thread_list=[]
#
#         thread_list = []  # 当所有线程运行完清空线程池
#
# print("总共用时:" + str(time.time() - start_time))