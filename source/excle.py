import time
import xlwt


class ExcelWrite:
    # 操作新建和写入excle
    def __init__(self, filename):
        """初始化表格列"""
        self.filename = filename
        self.stock_column = 1
        self.excel_book = xlwt.Workbook(encoding='utf-8')
        self.table_sheet = self.excel_book.add_sheet('Today_market')
        self.table_sheet.write(0, 0, '代码')
        self.table_sheet.write(0, 1, '名称')
        self.table_sheet.write(0, 2, '最新价')
        self.table_sheet.write(0, 3, '涨跌幅(%)')
        self.table_sheet.write(0, 4, '涨跌额')
        self.table_sheet.write(0, 5, '成交量')
        self.table_sheet.write(0, 6, '成交额')
        self.table_sheet.write(0, 7, '振幅(%)')
        self.table_sheet.write(0, 8, '最高')
        self.table_sheet.write(0, 9, '最低')
        self.table_sheet.write(0, 10, '今开')
        self.table_sheet.write(0, 11, '昨收')
        self.table_sheet.write(0, 12, '量比')
        self.table_sheet.write(0, 13, '换手率(%)')
        self.table_sheet.write(0, 14, '市盈率')
        self.table_sheet.write(0, 15, '市净率')

    def time_stamp(self):
        """返回当天日期"""
        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        return otherStyleTime

    def write_sheet(self, stock_list):
        """写入股票列表数据"""
        if len(stock_list) != 0:
            for stock in stock_list:
                self.table_sheet.write(self.stock_column, 0, stock["f12"])
                self.table_sheet.write(self.stock_column, 1, stock["f14"])
                self.table_sheet.write(self.stock_column, 2, stock["f2"])
                self.table_sheet.write(self.stock_column, 3, stock["f3"])
                self.table_sheet.write(self.stock_column, 4, stock["f4"])
                self.table_sheet.write(self.stock_column, 5, stock["f5"])
                self.table_sheet.write(self.stock_column, 6, stock["f6"])
                self.table_sheet.write(self.stock_column, 7, stock["f7"])
                self.table_sheet.write(self.stock_column, 8, stock["f15"])
                self.table_sheet.write(self.stock_column, 9, stock["f16"])
                self.table_sheet.write(self.stock_column, 10, stock["f17"])
                self.table_sheet.write(self.stock_column, 11, stock["f18"])
                self.table_sheet.write(self.stock_column, 12, stock["f10"])
                self.table_sheet.write(self.stock_column, 13, stock["f8"])
                self.table_sheet.write(self.stock_column, 14, stock["f9"])
                self.table_sheet.write(self.stock_column, 15, stock["f23"])
                self.stock_column = self.stock_column+1

    def save_book(self):
        """保持表格"""
        file_name = self.time_stamp() + self.filename+'.xls'
        self.excel_book.save('E:\\股票\\日交易\\'+self.time_stamp() + self.filename+'.xls')
        print('创建文件：'+file_name+'成功')
















