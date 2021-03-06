#! /usr/bin/python
# -*- coding: UTF-8 -*-

"""

    作者: 小肥巴巴
    简书: https://www.jianshu.com/u/db796a501972
    邮箱: imyunshi@163.com
    github: https://github.com/xiaofeipapa/python_example

    您可以任意转载, 恳请保留我作为原作者, 谢谢.

"""
import time

import pymysql
from timeit import default_timer
from DBUtils.PooledDB import PooledDB
import traceback
from DB_thread import DB_threading



class DMysqlConfig:
    """

        :param mincached:连接池中空闲连接的初始数量
        :param maxcached:连接池中空闲连接的最大数量
        :param maxshared:共享连接的最大数量
        :param maxconnections:创建连接池的最大数量
        :param blocking:超过最大连接数量时候的表现，为True等待连接数量下降，为false直接报错处理
        :param maxusage:单个连接的最大重复使用次数
        :param setsession:optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        :param reset:how connections should be reset when returned to the pool
            (False or None to rollback transcations started with begin(),
            True to always issue a rollback for safety's sake)
        :param host:数据库ip地址
        :param port:数据库端口
        :param db:库名
        :param user:用户名
        :param passwd:密码
        :param charset:字符编码
    """

    def __init__(self, host, db, user, password, port=3306):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password

        self.charset = 'UTF8'  # 不能是 utf-8
        self.minCached = 10
        self.maxCached = 20
        self.maxShared = 10
        self.maxConnection = 100

        self.blocking = True
        self.maxUsage = 100
        self.setSession = None
        self.reset = True


# ---- 用连接池来返回数据库连接
class DMysqlPoolConn:

    __pool = None

    def __init__(self, config):

        if not self.__pool:
            self.__class__.__pool = PooledDB(creator=pymysql,
                                             maxconnections=config.maxConnection,
                                             mincached=config.minCached,
                                             maxcached=config.maxCached,
                                             maxshared=config.maxShared,
                                             blocking=config.blocking,
                                             maxusage=config.maxUsage,
                                             setsession=config.setSession,
                                             charset=config.charset,
                                             host=config.host,
                                             port=config.port,
                                             database=config.db,
                                             user=config.user,
                                             password=config.password,
                                             )


    def get_pool(self):
        return self.__class__.__pool

    def get_conn(self):
        return self.__pool.connection()


# ========== 在程序的开始初始化一个连接池
host = 'localhost'
port = 3306
db = 'atock'
user = 'root'
password = '13549812386'

db_config = DMysqlConfig(host, db, user, password, port)


g_pool_connection = DMysqlPoolConn(db_config)


# ---- 使用 with 的方式来优化代码
class UsingMysql(object):

    def __init__(self, commit=True, log_time=True, log_label='总用时'):
        """

        :param commit: 是否在最后提交事务(设置为False的时候方便单元测试)
        :param log_time:  是否打印程序运行总时间
        :param log_label:  自定义log的文字
        """
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label

    def __enter__(self):

        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()

        # 从连接池获取数据库连接
        conn = g_pool_connection.get_conn()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        conn.autocommit = False

        self._conn = conn
        self._cursor = cursor
        return self

    def __exit__(self, *exc_info):
        # 提交事务
        # 在退出的时候自动关闭连接和cursor
        self._cursor.close()
        self._conn.close()

        if self._log_time is True:
            diff = default_timer() - self._start
            print('-- %s: %.6f 秒' % (self._log_label, diff))

    # ========= 一系列封装的业务方法

    # 返回 count
    def get_count(self, sql, params=None, count_key='count(id)'):
        """
        统计数量
        return:查询字段列表
        """
        self.cursor.execute(sql, params)
        data = self.cursor.fetchone()
        if self._commit:
            self._conn.commit()
        if not data:
            return 0
        return data[count_key]

    def fetch_one(self, sql, params=None):
        """
        返回第一条查询结果
        """
        self.cursor.execute(sql, params)
        if self._commit:
            self._conn.commit()
        return self.cursor.fetc

    def fetch_all(self, sql, params=None):
        """
        返回所有查询结果
        """
        self.cursor.execute(sql, params)
        if self._commit:
            self._conn.commit()
        return self.cursor.fetchall()

    def fetch_by_pk(self, sql, pk):
        self.cursor.execute(sql, (pk,))
        if self._commit:
            self._conn.commit()
        return self.cursor.fetchall()

    def update_by_pk(self, sql, params=None):
        """
        update数据库
        """
        # print(sql)
        self.cursor.execute(sql, params)
        if self._commit:
            self._conn.commit()

    def install_one(self, sql, params=None):
        """插入数据库"""
        self.cursor.execute(sql, params)
        if self._commit:
            self._conn.commit()

    def update_many(self, temp, data):
        try:
            self.cursor.executemany(temp, data)
            self._conn.commit()
        except:
            self.cursor.rollback()
            traceback.print_exc()

    def delete(self, sql, params=None):
        """
        delete数据库
        """
        # print(sql)
        self.cursor.execute(sql, params)
        if self._commit:
            self._conn.commit()

    def DB_thread(self):
        start_time = time.time()
        thread_list = []  # 创建线程池
        for i in range(1000):
            thread_list.append(DB_threading(i,))
            if len(thread_list) >= 1000:  # 当列表中的线程有10个,就开始执行10个线程
                print("线程数量为", len(thread_list))
                print(i)
                for thread in thread_list:
                    thread.start()

                for thread in thread_list:
                    thread.join()  # 10个线程都等待执行完,也就是说,10个线程有一个线程没运行完就不能往下执行代码; 这里会阻塞后面的thread_list=[]和print。但是多个线程间的join和join不会阻塞，也就是说执行完一个join还可以马上执行下一个join，但是执行完最后一个join不能马上执行 thread_list=[]

                thread_list = []  # 当所有线程运行完清空线程池

        print("总共用时:" + str(time.time() - start_time))

    def get_cursor(self):
        return self._cursor

    @property
    def cursor(self):
        return self._cursor