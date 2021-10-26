from source.tool import Tool


class atockTrendCount:
    def __init__(self, atock_data, days):
        """
        atock_data:股票名称、代码、日交易数据列表
        days：统计的最后天数
        """
        self.atock_data = atock_data
        self.days = days

    def get_count(self):
        """
        计算股票最近几天支撑与压力对比
        """
        atock_klines_count = []
        for atock in self.atock_data:
            atock_count_dict = {}
            self.atock_number = atock['stock_number']
            self.stock_name = atock['name']
            self.klines = atock['klines'].replace('[', '').replace(']', '').split(', ')
            count_dict = {}
            day = 5
            if len(self.klines) >= 5:
                statistical_period = self.klines[len(self.klines) - self.days:len(self.klines)]
                for i in statistical_period:
                    kline_list = i.split(",")
                    zhangDieFu = float(kline_list[8]) / 100
                    zuiGaoJia = float(kline_list[3])
                    shouPanJia = float(kline_list[2])
                    zuiDiJia = float(kline_list[4])
                    kaiPanJia = float(kline_list[1])
                    zhenFu = float(kline_list[7])
                    zhenFu = [zhenFu, 0.001][zhenFu == 0]
                    if zhangDieFu >= 0:
                        shangYaLiXian = zuiGaoJia - shouPanJia
                        xiaZhiChengXian = shouPanJia - zuiDiJia
                        count = ((xiaZhiChengXian - shangYaLiXian) / (
                                shouPanJia / (1 + zhangDieFu)) * 100) / zhenFu * 100
                    else:
                        shangYaLiXian = zuiGaoJia - shouPanJia
                        xiaZhiChengXian = shouPanJia - zuiDiJia
                        count = (((xiaZhiChengXian - shangYaLiXian) / (
                                shouPanJia / (1 + zhangDieFu)) * 100) / zhenFu * 100)
                    count = ("%.2f" % count)
                    day_key = '前' + str(day) + '日'
                    count_dict.update({day_key: count})
                    day = day - 1
                atock_count_dict.update({'atock_number': self.atock_number})
                atock_count_dict.update({'stock_name': self.stock_name})
                atock_count_dict.update(count_dict)
                atock_klines_count.append(atock_count_dict)
            else:
                print(self.stock_name + ' atock linbes is not in statisticalperiod')
        return atock_klines_count

    def get_price_margin(self):
        """
        获取交易天内股票价格变化
        rise_atio：指定天内上涨天数占比
        return：股票价格变化差额列表
        """
        atock_price_margin = []
        for atock in self.atock_data:
            atock_count_dict = {}
            atock_number = atock['stock_number']
            stock_name = atock['name']
            ndustry = atock['concept']
            Market_value_rank = atock["Market_value_rank"]
            profit_rank = atock["profit_rank"]
            nterprise_sum = atock["nterprise_sum"]
            klines = atock['klines'].replace('[', '').replace(']', '').split(', ')
            if len(klines) >= self.days:
                statistical_period = klines[len(klines) - self.days:len(klines)]
                statistical_period = Tool().spilt_str_list(statistical_period)
                # 判断成交量最低的那天是不是涨跌幅最低的那天
                quote_change = float(statistical_period[0][8])
                turnover_rate = float(statistical_period[0][10])
                a1 = 0
                a2 = 0
                for change1 in statistical_period:
                    if float(change1[8]) <= quote_change:
                        quote_change = float(change1[8])
                        serial_number1 = a1
                    a1 = a1 + 1
                for change2 in statistical_period:
                    if float(change2[10]) <= turnover_rate:
                        turnover_rate = float(change2[10])
                        serial_number2 = a2
                    a2 = a2 + 1
                if serial_number1 == serial_number2:
                    # 计算上涨天数占比
                    n = 0
                    rise_atio = 0
                    for change3 in statistical_period:
                        if float(change3[8]) > 0:
                            n = n + 1
                    rise_atio = n / self.days * 100
                    # 计算指定时间内最低价与现价的比率
                    lowest_price = float(statistical_period[0][4])
                    for change4 in statistical_period:
                        if float(change4[4]) <= lowest_price:
                            lowest_price = float(change4[4])
                    increase = float(change4[4])*100/lowest_price
                    atock_count_dict.update({'股票代码': atock_number})
                    atock_count_dict.update({'股票名称': stock_name})
                    atock_count_dict.update({'上涨天数占比': rise_atio})
                    atock_count_dict.update({'最低价与现价比率': increase})
                    atock_count_dict.update({'股票概念': ndustry})
                    atock_count_dict.update({'市值排名': Market_value_rank})
                    atock_count_dict.update({'利润排名': profit_rank})
                    atock_count_dict.update({'企业总数': nterprise_sum})
                    atock_price_margin.append(atock_count_dict)
                else:
                    continue
        return atock_price_margin

    def get_stock_doji(self):
        """
        获取最近下跌过程中十字星的股票
        """
        atock_price_margin = []
        for atock in self.atock_data:
            atock_count_dict = {}
            atock_number = atock['stock_number']
            stock_name = atock['name']
            concept = atock['concept']
            klines = atock['klines'].replace('[', '').replace(']', '').split(', ')
            if len(klines) >= self.days:
                statistical_period = klines[len(klines) - self.days:len(klines)]
                statistical_period = Tool().spilt_str_list(statistical_period)
                difference1 = 0
                difference2 = 0
                # if (float(statistical_period[len(statistical_period)-2][8]) < 0) and (float(statistical_period[len(statistical_period)-1][8]) > 0):
                if (float(statistical_period[len(statistical_period) - 1][8]) < 0):
                    a1 = (float(statistical_period[len(statistical_period)-2][1]) - float(statistical_period[len(statistical_period)-2][2]))
                    a1 = [a1, 1000000][a1 == 0]
                    difference1 = (float(statistical_period[len(statistical_period)-2][3]) - float(statistical_period[len(statistical_period)-2][4]))/a1
                # elif (float(statistical_period[len(statistical_period)-3][8])) < 0 and (float(statistical_period[len(statistical_period)-1][8]) > 0):
                #     a2 = (float(statistical_period[len(statistical_period) - 3][1]) - float(
                #         statistical_period[len(statistical_period) - 3][2]))
                #     a2 = [a2, 1000000][a2 == 0]
                #     difference2 = (float(statistical_period[len(statistical_period)-3][3]) - float(statistical_period[len(statistical_period)-3][4]))/a2
                else:
                    continue
                    # 判断最后2天收盘价与开盘价的差与幅度的比
                if difference1 >= 1:
                    turnover_rate1 = float(statistical_period[len(statistical_period)-1][10])
                    rate = turnover_rate1
                    turnover_rate = turnover_rate1
                    for change1 in statistical_period:
                        if float(change1[10]) <= turnover_rate:
                            turnover_rate = float(change1[10])
                        else:
                            continue
                    if turnover_rate >= rate:
                        atock_count_dict.update({'股票代码': atock_number})
                        atock_count_dict.update({'股票名称': stock_name})
                        atock_count_dict.update({'股票概念': concept})
                        atock_count_dict.update({'最近1天最小跌幅': float(statistical_period[len(statistical_period)-1][8])})
                        atock_price_margin.append(atock_count_dict)
                else:
                    continue
        return atock_price_margin

    def get_rise_stock(self):
        """
        获取最近下走势良好的股票
        """
        atock_price_margin = []
        for atock in self.atock_data:
            atock_count_dict = {}
            atock_number = atock['stock_number']
            stock_name = atock['name']
            concept = atock['concept']
            Market_value_rank = atock["Market_value_rank"]
            profit_rank = atock["profit_rank"]
            nterprise_sum = atock["nterprise_sum"]
            klines = atock['klines'].replace('[', '').replace(']', '').split(', ')
            if len(klines) >= self.days:
                statistical_period = klines[len(klines) - self.days:len(klines)]
                statistical_period = Tool().spilt_str_list(statistical_period)
                n = 0
                for stock_kline in statistical_period:
                    if float(stock_kline[8]) > 0:
                        n = n + 1
                    else:
                        continue
                b = len(statistical_period) - self.days-1
                a1 = float(statistical_period[len(statistical_period) - self.days-1][2])
                a2 = float(statistical_period[len(statistical_period)-1][2])
                Increase = (float(statistical_period[len(statistical_period) -1][2]) - float(statistical_period[len(statistical_period) - self.days][2]))/float(statistical_period[len(statistical_period) - self.days][2]) * 100
                ratio = int(n/self.days*100)
                atock_count_dict.update({"atock_number": atock_number, "stock_name": stock_name, "上涨天数比例": ratio, "上涨幅度": int(Increase), "concept": concept,"市值排名":Market_value_rank,"利润排名":profit_rank,"行业内企业总数":nterprise_sum})
                atock_price_margin.append(atock_count_dict)
        return atock_price_margin

    def get_breakthrough_stock(self):
        """
        获取最近5日均线突破10日均线的股票
        """
        atock_price_margin = []
        breakthrough_flag = 0
        for atock in self.atock_data:
            atock_count_dict = {}
            ten_day_price_sum = 0
            atock_number = atock['stock_number']
            stock_name = atock['name']
            concept = atock['concept']
            Market_value_rank = atock["Market_value_rank"]
            profit_rank = atock["profit_rank"]
            nterprise_sum = atock["nterprise_sum"]
            klines = atock['klines'].replace('[', '').replace(']', '').split(', ')
            if len(klines) >= 10:
                statistical_period = klines[len(klines) - 10:len(klines)]
                statistical_period = Tool().spilt_str_list(statistical_period)
                for price_message in statistical_period:
                    ten_day_price_sum = ten_day_price_sum + float(price_message[2])
                ten_day_price = ten_day_price_sum/10
                final_five_day_price_sum = 0
                for i in range(5, 10):
                    final_five_day_price_sum = final_five_day_price_sum + float(statistical_period[i][2])
                final_five_day_price = final_five_day_price_sum/5
                last_five_day_price_sum = 0
                for i in range(4, 9):
                    last_five_day_price_sum = last_five_day_price_sum + float(statistical_period[i][2])
                last_five_day_price = last_five_day_price_sum / 5
                last_last_five_day_price_sum = 0
                for i in range(3, 8):
                    last_last_five_day_price_sum = last_last_five_day_price_sum + float(statistical_period[i][2])
                last_last_five_day_price = last_last_five_day_price_sum / 5
                last_Slope = last_five_day_price - last_last_five_day_price
                final_Slope = final_five_day_price - last_five_day_price
                if (ten_day_price <= final_five_day_price < ten_day_price*1.01) and (last_five_day_price < final_five_day_price) and (final_Slope > last_Slope):
                    breakthrough_flag = 1
                else:
                    breakthrough_flag = 0

            if (len(klines) >= self.days) and (breakthrough_flag == 1):
                statistical_period = klines[len(klines) - self.days:len(klines)]
                statistical_period = Tool().spilt_str_list(statistical_period)
                n = 0
                for stock_kline in statistical_period:
                    if float(stock_kline[8]) > 0:
                        n = n + 1
                    else:
                        continue
                Increase = (float(statistical_period[len(statistical_period) -1][2]) - float(statistical_period[len(statistical_period) - self.days][2]))/float(statistical_period[len(statistical_period) - self.days][2]) * 100
                ratio = int(n/self.days*100)
                atock_count_dict.update({"atock_number": atock_number, "stock_name": stock_name, "上涨天数比例": ratio, "上涨幅度": int(Increase), "concept": concept,"市值排名":Market_value_rank,"利润排名":profit_rank,"行业内企业总数":nterprise_sum})
                atock_price_margin.append(atock_count_dict)
        if (400 >= len(atock_price_margin) >= 10):
            return atock_price_margin
        else:

            print('数组长度' + str(len(atock_price_margin)))
            atock_price_margin = []
            return atock_price_margin
