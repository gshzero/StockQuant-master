import time
import xlwt


class ExcelWrite:
    # 操作新建和写入excle
    def __init__(self, filename, data):
        """初始化表格列
        filename：保存的excel文件名称
        data：写入的数据字典
        """
        if len(data) != 0:
            self.filename = filename
            self.data = data
            self.stock_column = 1
            self.excel_book = xlwt.Workbook(encoding='utf-8')
            self.table_sheet = self.excel_book.add_sheet('data')
            n = 0
            for key in self.data[0]:
                self.table_sheet.write(0, n, key)
                n = n + 1
        else:
            print('输入数组为空')

    def time_stamp(self):
        """返回当天日期"""
        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        return otherStyleTime

    def write_sheet(self):
        """写入股票列表数据"""
        if len(self.data) != 0:
            for atock_dict in self.data:
                row_n = 0
                for value in atock_dict.values():
                    self.table_sheet.write(self.stock_column, row_n, str(value))
                    row_n = row_n + 1
                self.stock_column = self.stock_column+1

    def save_book(self):
        """保持表格"""
        file_name = self.time_stamp() + self.filename+'.xls'
        self.excel_book.save('E:\\股票\\日交易\\'+self.time_stamp() + self.filename+'.xls')
        print('创建文件：'+file_name+'成功')
















