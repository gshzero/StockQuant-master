
class Global_Data:
    def __init__(self):
        self.stock_klines_list = []

    def add_stock_klines_list(self,stock_klines):
        self.stock_klines_list.append(stock_klines)

    def get_stock_klines_list(self):
        return self.stock_klines_list