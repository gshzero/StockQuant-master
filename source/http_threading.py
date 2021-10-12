import os, threading
from HttpConnet import HttpConnet
from globalvar import Global_Data


class Http_Threading(threading.Thread):
    def __init__(self, date, stock_data):
        super(Http_Threading, self).__init__()
        self.object = HttpConnet()
        self.global_data = date
        self.stock =stock_data

    def run(self):
        stock_date = self.object.get_stock_klines(self.stock['f12'])
        if stock_date is not None:
            self.global_data.add_stock_klines_list(stock_date)