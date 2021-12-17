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
        获取最新一天下跌且成交量缩小的股票交易天内股票价格变化
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
                lastest_day = statistical_period[(len(statistical_period) - 1)][0]
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
                    # 计算开盘价与最低价的差减去最高价与收盘价的差
                    price_strength = (float(change1[1]) - float(change1[4])) - (float(change1[3]) - float(change1[2]))
                if (serial_number1 == serial_number2 == (len(statistical_period) - 1)) and (price_strength >= 0):
                    # 计算上涨天数占比
                    n = 0
                    for change3 in statistical_period:
                        if float(change3[8]) > 0:
                            n = n + 1
                    rise_atio = n / self.days * 100
                    # 计算指定时间内最低价与现价的比率
                    lowest_price = float(statistical_period[0][4])
                    for change4 in statistical_period:
                        if float(change4[4]) <= lowest_price:
                            lowest_price = float(change4[4])
                    increase = float(change4[4]) * 100 / lowest_price
                    atock_count_dict.update({'股票代码': atock_number})
                    atock_count_dict.update({'股票名称': stock_name})
                    atock_count_dict.update({'上涨天数占比': rise_atio})
                    atock_count_dict.update({'最低价与现价比率': increase})
                    atock_count_dict.update({'股票概念': ndustry})
                    atock_count_dict.update({'市值排名': Market_value_rank})
                    atock_count_dict.update({'利润排名': profit_rank})
                    atock_count_dict.update({'企业总数': nterprise_sum})
                    atock_count_dict.update({'最后交易日': lastest_day})
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
            day_statistical_period = Tool().spilt_str_list(klines)
            moon_klines = atock['moon_klines'].replace('[', '').replace(']', '').split(', ')
            week_klines = atock['week_klines'].replace('[', '').replace(']', '').split(', ')
            if len(moon_klines) >= 10:
                statistical_period = klines[len(klines) - self.days:len(klines)]
                statistical_period = Tool().spilt_str_list(statistical_period)
                week_statistical_period = week_klines[len(week_klines) - 10:len(week_klines)]
                week_statistical_period = Tool().spilt_str_list(week_statistical_period)
                moon_statistical_period = moon_klines[len(moon_klines) - 10:len(moon_klines)]
                moon_statistical_period = Tool().spilt_str_list(moon_statistical_period)
            else:
                continue
            #计算月均线价
            if len(moon_klines) >= 10:
                moon_lastest_day = moon_statistical_period[(len(moon_statistical_period) - 1)][0]
                moon_first_day = moon_statistical_period[(len(moon_statistical_period) - 5)][0]
                # 计算最近5个月均线价
                final_five_moon_price_sum = 0
                for i in range(5, 10):
                    final_five_moon_price_sum = final_five_moon_price_sum + float(moon_statistical_period[i][2])
                final_five_moon_price = final_five_moon_price_sum / 5
                if float(statistical_period[len(statistical_period) - 2][2]) > final_five_moon_price:
                    over_moon_flag = '旧突破'
                elif float(statistical_period[len(statistical_period) - 2][2]) < final_five_moon_price < float(
                        statistical_period[len(statistical_period) - 1][2]):
                    over_moon_flag = '今突破'
                else:
                    over_moon_flag = '未突破'


            else:
                final_five_moon_price = 1000000
                moon_lastest_day = "none"
                moon_first_day = "none"
                over_moon_flag = '失效'
                #计算5周均线价
            if len(week_klines) >= 10:
                week_lastest_day = week_statistical_period[(len(week_statistical_period) - 1)][0]
                week_first_day = week_statistical_period[(len(week_statistical_period) - 5)][0]
                # 计算最近5个月均线价
                final_five_week_price_sum = 0
                for i in range(5, 10):
                    final_five_week_price_sum = final_five_week_price_sum + float(week_statistical_period[i][2])
                final_five_week_price = final_five_week_price_sum / 5
                if float(statistical_period[len(statistical_period) - 2][2]) > final_five_week_price:
                    over_week_flag = '周旧突破'
                elif float(statistical_period[len(statistical_period) - 2][2]) < final_five_week_price < float(
                        statistical_period[len(statistical_period) - 1][2]):
                    over_week_flag = '周今突破'
                else:
                    over_week_flag = '周未突破'
            else:
                final_five_week_price = 1000000
                week_lastest_day = "none"
                week_first_day = "none"
                over_week_flag = '失效'
                # 判断日线情况
            if len(klines) >= self.days:
                lastest_day = statistical_period[(len(statistical_period) - 1)][0]
                lastest_day_shoudiepancha = float(statistical_period[len(statistical_period) - 1][1]) - float(
                    statistical_period[len(statistical_period) - 1][2])
                lastest_day_zuigaojiagecha = float(statistical_period[len(statistical_period) - 1][3]) - float(
                    statistical_period[len(statistical_period) - 1][4])
                dao_shu_di_er_tian_shoudiepancha = float(statistical_period[len(statistical_period) - 2][1]) - float(
                    statistical_period[len(statistical_period) - 2][2])
                if lastest_day_shoudiepancha == 0:
                    lastest_day_shoudiepancha = 10000
                    lastest_day_zuigaojiagecha = 10000
                if lastest_day_shoudiepancha < 0:
                    lastest_day_shangyinxian = float(statistical_period[len(statistical_period) - 1][3]) - float(
                        statistical_period[len(statistical_period) - 1][2])
                    lastest_day_shangyinxianbili = lastest_day_shangyinxian / lastest_day_zuigaojiagecha
                elif lastest_day_shoudiepancha > 0:
                    lastest_day_xiayinxian = float(statistical_period[len(statistical_period) - 1][2]) - float(
                        statistical_period[len(statistical_period) - 1][4])
                    lastest_day_xiayinxianbili = lastest_day_xiayinxian / lastest_day_zuigaojiagecha
                else:
                    continue
                if (lastest_day_shoudiepancha < 0) and (lastest_day_shangyinxianbili <= 0.2) and (
                        float(statistical_period[len(statistical_period) - 1][8]) <= 9.00) and (
                        dao_shu_di_er_tian_shoudiepancha >= 0) and (
                        abs(dao_shu_di_er_tian_shoudiepancha) < abs(lastest_day_shoudiepancha)):
                    a1 = 0
                    a2 = 0
                    for change2 in statistical_period:
                        a2 = a2 + float(change2[10])
                        if (float(change2[1]) - float(change2[2])) < 0:
                            a1 = a1 + 1
                    a2 = a2 / len(statistical_period)
                    # 校验最后一天成交率
                    if a2 * 0.6 < float(change2[10]) < a2 * 2:
                        stock_Pressure_level_dict = self.get_stock_Pressure_level(day_statistical_period)
                        atock_count_dict.update({'股票代码': atock_number})
                        atock_count_dict.update({'股票名称': stock_name})
                        atock_count_dict.update({'股票概念': concept})
                        atock_count_dict.update({'最近红柱天数比例': a1 / len(statistical_period) * 100})
                        atock_count_dict.update({'最近1天最低价与收盘价差': (float(
                            statistical_period[len(statistical_period) - 1][2]) - float(
                            statistical_period[len(statistical_period) - 1][4])) / float(
                            statistical_period[len(statistical_period) - 2][2]) * 100})
                        atock_count_dict.update({'最后交易日': lastest_day})
                        atock_count_dict.update({'周均价最后周': week_lastest_day})
                        atock_count_dict.update({'周均价第一周': week_first_day})
                        atock_count_dict.update({'距离周均价比率':  (float(
                            statistical_period[len(statistical_period) - 1][2]) - final_five_week_price) / float(
                            statistical_period[len(statistical_period) - 1][2]) * 100})
                        atock_count_dict.update({'周均价突破2%': final_five_week_price * 1.02})
                        atock_count_dict.update({'是否今天突破周均价': over_week_flag})
                        atock_count_dict.update({'距离月均线百分比': (float(
                            statistical_period[len(statistical_period) - 1][2]) - final_five_moon_price) / float(
                            statistical_period[len(statistical_period) - 1][2]) * 100})
                        atock_count_dict.update({'月均价突破2%': final_five_moon_price * 1.02})
                        atock_count_dict.update({'月均价最后月份': moon_lastest_day})
                        atock_count_dict.update({'月均价第一月份': moon_first_day})
                        atock_count_dict.update({'是否今天突破月均价': over_moon_flag})
                        atock_count_dict.update({"压力位差率": stock_Pressure_level_dict["压力位差率"]})
                        atock_count_dict.update({"支撑位差率": stock_Pressure_level_dict["支撑位差率"]})
                        atock_count_dict.update({"乖离率": stock_Pressure_level_dict["乖离率"]})
                        atock_price_margin.append(atock_count_dict)
                elif (lastest_day_shoudiepancha > 0) and (lastest_day_xiayinxianbili >= 0.6) and (
                        dao_shu_di_er_tian_shoudiepancha > 0) and (
                        float(statistical_period[len(statistical_period) - 1][8]) <= 9.00) and (
                        abs(dao_shu_di_er_tian_shoudiepancha) > abs(lastest_day_shoudiepancha)):
                    a1 = 0
                    a2 = 0
                    for change2 in statistical_period:
                        a2 = a2 + float(change2[10])
                        if (float(change2[1]) - float(change2[2])) < 0:
                            a1 = a1 + 1
                    a2 = a2 / len(statistical_period)
                    # 校验最后一天成交率
                    if a2 * 0.6 < float(change2[10]) < a2 * 2:
                        stock_Pressure_level_dict = self.get_stock_Pressure_level(day_statistical_period)
                        atock_count_dict.update({'股票代码': atock_number})
                        atock_count_dict.update({'股票名称': stock_name})
                        atock_count_dict.update({'股票概念': concept})
                        atock_count_dict.update({'最近红柱天数比例': a1 / len(statistical_period) * 100})
                        atock_count_dict.update({'最近1天最低价与收盘价差': (float(
                            statistical_period[len(statistical_period) - 1][2]) - float(
                            statistical_period[len(statistical_period) - 1][4])) / float(
                            statistical_period[len(statistical_period) - 2][2]) * 100})
                        atock_count_dict.update({'最后交易日': lastest_day})
                        atock_count_dict.update({'周均价最后周': week_lastest_day})
                        atock_count_dict.update({'周均价第一周': week_first_day})
                        atock_count_dict.update({'距离周均价比率':  (float(
                            statistical_period[len(statistical_period) - 1][2]) - final_five_week_price) / float(
                            statistical_period[len(statistical_period) - 1][2]) * 100})
                        atock_count_dict.update({'周均价突破2%': final_five_week_price * 1.02})
                        atock_count_dict.update({'是否今天突破周均价': over_week_flag})
                        atock_count_dict.update({'距离月均线百分比': (float(
                            statistical_period[len(statistical_period) - 1][2]) - final_five_moon_price) / float(
                            statistical_period[len(statistical_period) - 1][2]) * 100})
                        atock_count_dict.update({'月均价突破2%': final_five_moon_price * 1.02})
                        atock_count_dict.update({'月均价最后月份': moon_lastest_day})
                        atock_count_dict.update({'月均价第一月份': moon_first_day})
                        atock_count_dict.update({'是否今天突破月均价': over_moon_flag})
                        atock_count_dict.update({"压力位差率": stock_Pressure_level_dict["压力位差率"]})
                        atock_count_dict.update({"支撑位差率": stock_Pressure_level_dict["支撑位差率"]})
                        atock_count_dict.update({"乖离率": stock_Pressure_level_dict["乖离率"]})
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
                lastest_day = statistical_period[(len(statistical_period) - 1)][0]
                n = 0
                for stock_kline in statistical_period:
                    if float(stock_kline[8]) > 0:
                        n = n + 1
                    else:
                        continue
                # if float(stock_kline[8]) > 0:
                if 1 > 0:
                    b = len(statistical_period) - self.days - 1
                    a1 = float(statistical_period[len(statistical_period) - self.days - 1][2])
                    a2 = float(statistical_period[len(statistical_period) - 1][2])
                    Increase = (float(statistical_period[len(statistical_period) - 1][2]) - float(
                        statistical_period[len(statistical_period) - self.days][2])) / float(
                        statistical_period[len(statistical_period) - self.days][2]) * 100
                    ratio = int(n / self.days * 100)
                    atock_count_dict.update(
                        {"atock_number": atock_number, "stock_name": stock_name, "上涨天数比例": ratio, "上涨幅度": int(Increase),
                         "concept": concept, "市值排名": Market_value_rank, "利润排名": profit_rank, "行业内企业总数": nterprise_sum,
                         '最后交易日': lastest_day})
                    atock_price_margin.append(atock_count_dict)
                else:
                    continue
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
                lastest_day = statistical_period[(len(statistical_period) - 1)][0]
                for price_message in statistical_period:
                    ten_day_price_sum = ten_day_price_sum + float(price_message[2])
                ten_day_price = ten_day_price_sum / 10
                final_five_day_price_sum = 0
                # 计算最近3天5日均线确定5日均线是否上涨状态
                for i in range(5, 10):
                    final_five_day_price_sum = final_five_day_price_sum + float(statistical_period[i][2])
                final_five_day_price = final_five_day_price_sum / 5
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
                # 最后一天5日均线大于10日均线且大于前一天5日均线且最后2天的5日均线差大于倒数第二天与倒数第三天5日均线差
                if (ten_day_price >= final_five_day_price >= 0.95 * ten_day_price) and (
                        last_five_day_price < final_five_day_price) and (final_Slope > last_Slope) and (
                        float(statistical_period[9][2]) > ten_day_price) and (
                        float(statistical_period[9][2]) > final_five_day_price) and (
                        float(statistical_period[9][4]) < ten_day_price) and (
                        float(statistical_period[9][4]) < final_five_day_price):
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
                # 红柱
                if float(stock_kline[2]) - float(stock_kline[1]) > 0 and float(stock_kline[2]) < 9.00:
                    Increase = (float(statistical_period[len(statistical_period) - 1][2]) - float(
                        statistical_period[len(statistical_period) - 1][4])) / float(
                        statistical_period[len(statistical_period) - 2][2]) * 100
                    ratio = int(n / self.days * 100)
                    atock_count_dict.update(
                        {"atock_number": atock_number, "stock_name": stock_name, "上涨天数比例": ratio, "上涨幅度": int(Increase),
                         "concept": concept, "市值排名": Market_value_rank, "利润排名": profit_rank, "行业内企业总数": nterprise_sum,
                         '最后交易日': lastest_day})
                    atock_price_margin.append(atock_count_dict)
        if (400 >= len(atock_price_margin) >= 10):
            return atock_price_margin
        else:

            print('数组长度' + str(len(atock_price_margin)))
            atock_price_margin = []
            return atock_price_margin

    def get_over_five_moving_average_stock(self):
        """
        获取股票最近过5天线的比例
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
            if len(klines) >= self.days + 5:
                statistical_period = klines[len(klines) - (self.days + 5):len(klines)]
                statistical_period = Tool().spilt_str_list(statistical_period)
            for i in range(1, 9):
                print(1)

    def get_week_breakthrough_stock(self):
        """
        获取最近5周均线突破10周均线的股票
        """
        atock_price_margin = []
        breakthrough_flag = 0
        up_n = 0
        concept_dict = {}
        time_falg = 1
        for atock in self.atock_data:
            atock_count_dict = {}
            ten_week_price_sum = 0
            atock_number = atock['stock_number']
            stock_name = atock['name']
            concept = atock['concept']
            Market_value_rank = atock["Market_value_rank"]
            profit_rank = atock["profit_rank"]
            nterprise_sum = atock["nterprise_sum"]
            day_klines_full = atock['klines'].replace('[', '').replace(']', '').split(', ')
            moon_klines_full = atock['moon_klines'].replace('[', '').replace(']', '').split(', ')
            klines_full = atock['week_klines'].replace('[', '').replace(']', '').split(', ')
            klines = atock['week_klines'].replace('[', '').replace(']', '').split(', ')
            if len(moon_klines_full) >= 10:
                moon_statistical_period = moon_klines_full[len(moon_klines_full) - 10:len(moon_klines_full)]
                moon_statistical_period = Tool().spilt_str_list(moon_statistical_period)
                day_statistical_period = day_klines_full[len(day_klines_full) - 2:len(day_klines_full)]
                day_statistical_period = Tool().spilt_str_list(day_statistical_period)
                week_statistical_period = klines[len(klines) - 10:len(klines)]
                week_statistical_period = Tool().spilt_str_list(week_statistical_period)
            b = klines_full.pop()
            if len(moon_klines_full) >= 10:
                moon_lastest_day = moon_statistical_period[(len(moon_statistical_period) - 1)][0]
                moon_first_day = moon_statistical_period[(len(moon_statistical_period) - 5)][0]
                # 计算最近5个月均线价
                final_five_moon_price_sum = 0
                for i in range(5, 10):
                    final_five_moon_price_sum = final_five_moon_price_sum + float(moon_statistical_period[i][2])
                final_five_moon_price = final_five_moon_price_sum / 5
                if float(day_statistical_period[len(day_statistical_period)-2][2]) < final_five_moon_price < float(day_statistical_period[len(day_statistical_period)-1][2]):
                    moon_over_flag = "月均今天突破"
                elif final_five_moon_price > float(day_statistical_period[len(day_statistical_period)-1][2]):
                    moon_over_flag = "月均未突破"
                else:
                    moon_over_flag = "月均旧突破"
            else:
                final_five_moon_price = 1000000
                moon_lastest_day = "none"
                moon_first_day = "none"
                moon_over_flag = "失效"
            if len(klines) >= 10:
                zui_hou_yi_tian_shou_pan_jia = float(day_statistical_period[(len(day_statistical_period) - 1)][2])
                zdao_shu_di_er_tian_shou_pan_jia = float(day_statistical_period[(len(day_statistical_period) - 2)][2])
                lastest_week = week_statistical_period[(len(week_statistical_period) - 1)][0]
                first_week = week_statistical_period[(len(week_statistical_period) - 5)][0]
                if time_falg == 1:
                    lastest_week_falg = lastest_week
                    time_falg = time_falg + 1
                for price_message in week_statistical_period:
                    ten_week_price_sum = ten_week_price_sum + float(price_message[2])
                ten_week_price = ten_week_price_sum / 10
                final_five_week_price_sum = 0
                # 计算最近3周的周均线确定5周均线是否上涨状态
                for i in range(5, 10):
                    final_five_week_price_sum = final_five_week_price_sum + float(week_statistical_period[i][2])
                final_five_week_price = final_five_week_price_sum / 5
                last_five_week_price_sum = 0
                for i in range(4, 9):
                    last_five_week_price_sum = last_five_week_price_sum + float(week_statistical_period[i][2])
                last_five_week_price = last_five_week_price_sum / 5
                last_last_five_week_price_sum = 0
                for i in range(3, 8):
                    last_last_five_week_price_sum = last_last_five_week_price_sum + float(week_statistical_period[i][2])
                last_last_five_week_price = last_last_five_week_price_sum / 5
                last_Slope = last_five_week_price - last_last_five_week_price
                final_Slope = final_five_week_price - last_five_week_price
                # 最后一天5周均线小于10周均线且大于前一5周均线且最后2天的5日均线差大于倒数第二周与倒数第三周5周均线差
                if (ten_week_price <= final_five_week_price <= 1.1 * ten_week_price) and (
                        last_five_week_price < final_five_week_price) and (final_Slope > last_Slope) and (
                        float(week_statistical_period[9][2]) > ten_week_price) and (
                        float(week_statistical_period[9][2]) > final_five_week_price) and (
                        float(week_statistical_period[9][4]) < ten_week_price) and (
                        float(week_statistical_period[9][4]) < final_five_week_price) and (
                        float(week_statistical_period[8][2]) < final_five_week_price) and (
                        zui_hou_yi_tian_shou_pan_jia >= final_five_week_price) and (
                        zdao_shu_di_er_tian_shou_pan_jia < final_five_week_price):
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
                # 红柱
                if float(stock_kline[2]) - float(stock_kline[1]) > 0:
                    Increase = (float(statistical_period[len(statistical_period) - 1][2]) - float(
                        statistical_period[len(statistical_period) - 1][4])) / float(
                        statistical_period[len(statistical_period) - 2][2]) * 100
                    ratio = int(n / self.days * 100)
                    a = b.split(',')[8]
                    atock_count_dict.update(
                        {"atock_number": atock_number, "stock_name": stock_name, "上涨天数比例": ratio, "上涨幅度": int(Increase),
                         "concept": concept, "市值排名": Market_value_rank, "利润排名": profit_rank, "行业内企业总数": nterprise_sum,
                         '第一交易周': first_week,
                         '最后交易周': lastest_week_falg, '第一个月份': moon_first_day, '最后月份': moon_lastest_day, '最后一周涨幅': a,
                         '离月均线距离比率': (
                                                 zui_hou_yi_tian_shou_pan_jia - final_five_moon_price) / zui_hou_yi_tian_shou_pan_jia * 100,
                         '离周均线距离比率': (
                                                 zui_hou_yi_tian_shou_pan_jia - final_five_week_price) / final_five_week_price * 100,"月是否今天突破标记": moon_over_flag})
                    atock_price_margin.append(atock_count_dict)
                    concept_list = concept.split("，")
                    concept_list.pop()
                    if lastest_week_falg == lastest_week:
                        for i in concept_list:
                            if concept_dict.get(i, "Not Available") == "Not Available":
                                concept_dict.update({i: 1})
                            else:
                                concept_dict[i] = concept_dict[i] + 1
                    print(stock_name + " :" + a)
                    if float(a) > 0:
                        up_n = up_n + 1

        if (400 >= len(atock_price_margin) >= 1):
            print('up_n: ' + str(up_n))
            print(sorted(concept_dict.items(), key=lambda kv: (kv[1], kv[0])))
            return atock_price_margin
        else:

            print('数组长度' + str(len(atock_price_margin)))
            atock_price_margin = []
            return atock_price_margin

    def get_moon_breakthrough_stock(self):
        """
        获取最近5月均线突破10月均线的股票
        """
        atock_price_margin = []
        breakthrough_flag = 0
        up_n = 0
        concept_dict = {}
        time_falg = 1
        for atock in self.atock_data:
            atock_count_dict = {}
            ten_day_price_sum = 0
            atock_number = atock['stock_number']
            stock_name = atock['name']
            concept = atock['concept']
            Market_value_rank = atock["Market_value_rank"]
            profit_rank = atock["profit_rank"]
            nterprise_sum = atock["nterprise_sum"]
            day_klines_full = atock['klines'].replace('[', '').replace(']', '').split(', ')
            klines_full = atock['moon_klines'].replace('[', '').replace(']', '').split(', ')
            klines = atock['moon_klines'].replace('[', '').replace(']', '').split(', ')
            b = day_klines_full[len(day_klines_full) - 1]
            if len(klines) >= 10:
                statistical_period = klines[len(klines) - 10:len(klines)]
                day_statistical_period = day_klines_full[len(day_klines_full) - 2:len(day_klines_full)]
                day_statistical_period = Tool().spilt_str_list(day_statistical_period)
                zui_hou_yi_tian_shou_pan_jia = float(day_statistical_period[(len(day_statistical_period) - 1)][2])
                zdao_shu_di_er_tian_shou_pan_jia = float(day_statistical_period[(len(day_statistical_period) - 2)][2])
                statistical_period = Tool().spilt_str_list(statistical_period)
                lastest_day = statistical_period[(len(statistical_period) - 1)][0]
                first_day = statistical_period[(len(statistical_period) - 5)][0]
                if time_falg == 1:
                    lastest_day_falg = lastest_day
                    time_falg = time_falg + 1
                for price_message in statistical_period:
                    ten_day_price_sum = ten_day_price_sum + float(price_message[2])
                ten_day_price = ten_day_price_sum / 10
                final_five_day_price_sum = 0
                # 计算最近3周的周均线确定5周均线是否上涨状态
                for i in range(5, 10):
                    final_five_day_price_sum = final_five_day_price_sum + float(statistical_period[i][2])
                final_five_day_price = final_five_day_price_sum / 5
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
                # 最后一天5月均线小于10月均线且大于前一5月均线且最后2月的5月均线差大于倒数第二月与倒数第三月5月均线差
                if (ten_day_price <= final_five_day_price) and (
                        last_five_day_price < final_five_day_price) and (final_Slope > last_Slope) and (
                        float(statistical_period[9][2]) > ten_day_price) and (
                        float(statistical_period[9][2]) > final_five_day_price) and (
                        float(statistical_period[9][4]) < ten_day_price) and (
                        float(statistical_period[9][4]) < final_five_day_price) and (
                        float(statistical_period[8][2]) < final_five_day_price) and (
                        zui_hou_yi_tian_shou_pan_jia >= final_five_day_price) and (
                        zdao_shu_di_er_tian_shou_pan_jia < final_five_day_price):
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
                # 红柱
                if float(stock_kline[2]) - float(stock_kline[1]) > 0:
                    Increase = (float(statistical_period[len(statistical_period) - 1][2]) - float(
                        statistical_period[len(statistical_period) - 1][4])) / float(
                        statistical_period[len(statistical_period) - 2][2]) * 100
                    ratio = int(n / self.days * 100)
                    a = b.split(',')[8]
                    atock_count_dict.update(
                        {"atock_number": atock_number, "stock_name": stock_name, "上涨天数比例": ratio, "上涨幅度": int(Increase),
                         "concept": concept, "市值排名": Market_value_rank, "利润排名": profit_rank, "行业内企业总数": nterprise_sum,
                         '第一个月份': first_day,
                         '最后月份': lastest_day, '最后一周涨幅': a, '离月均线距离比率': (
                                                                                   zui_hou_yi_tian_shou_pan_jia - final_five_day_price) / zui_hou_yi_tian_shou_pan_jia * 100,
                         '月均线突破2%价': final_five_day_price * 1.02})
                    atock_price_margin.append(atock_count_dict)
                    concept_list = concept.split("，")
                    concept_list.pop()
                    if lastest_day_falg == lastest_day:
                        for i in concept_list:
                            if concept_dict.get(i, "Not Available") == "Not Available":
                                concept_dict.update({i: 1})
                            else:
                                concept_dict[i] = concept_dict[i] + 1
                    print(stock_name + " :" + a)
                    if float(a) > 0:
                        up_n = up_n + 1

        if (400 >= len(atock_price_margin) >= 1):
            print('up_n: ' + str(up_n))
            print(sorted(concept_dict.items(), key=lambda kv: (kv[1], kv[0])))
            return atock_price_margin
        else:

            print('数组长度' + str(len(atock_price_margin)))
            atock_price_margin = []
            return atock_price_margin

    def get_week_stock_doji(self):
        """
        获取最近下跌过程中十字星的股票
        """
        up_n = 0
        atock_price_margin = []
        for atock in self.atock_data:
            atock_count_dict = {}
            atock_number = atock['stock_number']
            stock_name = atock['name']
            concept = atock['concept']
            klines_full = atock['week_klines'].replace('[', '').replace(']', '').split(', ')
            klines = klines_full
            b = klines[len(klines) - 1]
            # print(b)
            if len(klines) >= 10:
                statistical_period = klines[len(klines) - 10:len(klines)]
                statistical_period = Tool().spilt_str_list(statistical_period)
                final_five_day_price_sum = 0
                # 计算最近3周的周均线确定5周均线是否上涨状态
                for i in range(5, 10):
                    final_five_day_price_sum = final_five_day_price_sum + float(statistical_period[i][2])
                final_five_day_price = final_five_day_price_sum / 5
            if len(klines) >= self.days:
                statistical_period = klines[len(klines) - self.days:len(klines)]
                statistical_period = Tool().spilt_str_list(statistical_period)
                lastest_day = statistical_period[(len(statistical_period) - 1)][0]
                lastest_day_shoudiepancha = float(statistical_period[len(statistical_period) - 1][1]) - float(
                    statistical_period[len(statistical_period) - 1][2])
                lastest_day_zuigaojiagecha = float(statistical_period[len(statistical_period) - 1][3]) - float(
                    statistical_period[len(statistical_period) - 1][4])
                dao_shu_di_er_tian_shoudiepancha = float(
                    statistical_period[len(statistical_period) - 2][1]) - float(
                    statistical_period[len(statistical_period) - 2][2])
                if lastest_day_shoudiepancha == 0:
                    lastest_day_shoudiepancha = 10000
                    lastest_day_zuigaojiagecha = 10000
                if lastest_day_shoudiepancha < 0:
                    lastest_day_shangyinxian = float(statistical_period[len(statistical_period) - 1][3]) - float(
                        statistical_period[len(statistical_period) - 1][2])
                    lastest_day_shangyinxianbili = lastest_day_shangyinxian / lastest_day_zuigaojiagecha
                elif lastest_day_shoudiepancha > 0:
                    lastest_day_xiayinxian = float(statistical_period[len(statistical_period) - 1][2]) - float(
                        statistical_period[len(statistical_period) - 1][4])
                    lastest_day_xiayinxianbili = lastest_day_xiayinxian / lastest_day_zuigaojiagecha
                else:
                    continue
                a = b.split(',')[8]
                if (lastest_day_shoudiepancha < 0) and (lastest_day_shangyinxianbili <= 0.3) and (
                        dao_shu_di_er_tian_shoudiepancha >= 0) and (
                        abs(dao_shu_di_er_tian_shoudiepancha) < abs(lastest_day_shoudiepancha)) and (
                        float(statistical_period[len(statistical_period) - 1][2]) > final_five_day_price):
                    a1 = 0
                    a2 = 0
                    for change2 in statistical_period:
                        a2 = a2 + float(change2[10])
                        if (float(change2[1]) - float(change2[2])) < 0:
                            a1 = a1 + 1
                    a2 = a2 / len(statistical_period)
                    # 校验最后一天成交率
                    if a2 * 0.6 < float(change2[10]) < a2 * 2:
                        atock_count_dict.update({'股票代码': atock_number})
                        atock_count_dict.update({'股票名称': stock_name})
                        atock_count_dict.update({'股票概念': concept})
                        atock_count_dict.update({'最近红柱比例': a1 / len(statistical_period) * 100})
                        atock_count_dict.update({'最近1天最低价与收盘价差': (float(
                            statistical_period[len(statistical_period) - 1][2]) - float(
                            statistical_period[len(statistical_period) - 1][4])) / float(
                            statistical_period[len(statistical_period) - 2][2]) * 100})
                        atock_count_dict.update({'最后交易日': lastest_day, "最后一周涨幅": a})
                        atock_price_margin.append(atock_count_dict)
                        if float(a) > 0:
                            up_n = up_n + 1
                elif (lastest_day_shoudiepancha > 0) and (lastest_day_xiayinxianbili >= 0.6) and (
                        dao_shu_di_er_tian_shoudiepancha > 0) and (
                        abs(dao_shu_di_er_tian_shoudiepancha) > abs(lastest_day_shoudiepancha)):
                    a1 = 0
                    a2 = 0
                    for change2 in statistical_period:
                        a2 = a2 + float(change2[10])
                        if (float(change2[1]) - float(change2[2])) < 0:
                            a1 = a1 + 1
                    a2 = a2 / len(statistical_period)
                    # 校验最后一天成交率
                    if a2 * 0.6 < float(change2[10]) < a2 * 2:
                        atock_count_dict.update({'股票代码': atock_number})
                        atock_count_dict.update({'股票名称': stock_name})
                        atock_count_dict.update({'股票概念': concept})
                        atock_count_dict.update({'最近红柱比例': a1 / len(statistical_period) * 100})
                        atock_count_dict.update({'最近1天最低价与收盘价差': (float(
                            statistical_period[len(statistical_period) - 1][2]) - float(
                            statistical_period[len(statistical_period) - 1][4])) / float(
                            statistical_period[len(statistical_period) - 2][2]) * 100})
                        atock_count_dict.update({'最后交易日': lastest_day, "最后一周涨幅": a})
                        atock_price_margin.append(atock_count_dict)
                        if float(a) > 0:
                            up_n = up_n + 1
                else:
                    continue
        print('up_n: ' + str(up_n))
        return atock_price_margin

    def get_stock_week_rise(self, week_count):
        """
        获取上周突破且最近2周红柱或绿柱缩量的股票列表
        """
        up_n = 0
        week_counts = week_count
        over_week_price_flag = 0
        atock_price_margin = []
        for atock in self.atock_data:
            atock_count_dict = {}
            first_week_over_flag = 0
            atock_number = atock['stock_number']
            stock_name = atock['name']
            concept = atock['concept']
            klines_full = atock['week_klines'].replace('[', '').replace(']', '').split(', ')
            klines = atock['week_klines'].replace('[', '').replace(']', '').split(', ')
            week_statistical_period = Tool().spilt_str_list(klines)
            day_klines = atock['klines'].replace('[', '').replace(']', '').split(', ')
            day_statistical_period = Tool().spilt_str_list(day_klines)
            now = klines_full.pop()
            klines.pop()
            try:
                now_price = now.split(",")[8]
            except:
                print(atock['name'])
                now_price = "none"
            # klines = klines_full
            # b = klines[len(klines) - 1]
            week_time_list = []
            for weeks in range(0, week_counts):
                week_time_list.append(weeks)
            week_time_list.reverse()
            if len(klines) >= 10+week_count:
                for week_time in week_time_list:
                    first_week = len(klines) - 10-week_time
                    lastest_week = len(klines)-week_time
                    statistical_period = klines[first_week:lastest_week]
                    statistical_period = Tool().spilt_str_list(statistical_period)
                    final_five_day_price_sum = 0
                    # 计算最近3周的周均线确定5周均线是否上涨状态
                    for i in range(5, 10):
                        final_five_day_price_sum = final_five_day_price_sum + float(statistical_period[i][2])
                    final_five_day_price = final_five_day_price_sum / 5
                    # 判断统计周期第一周是否突破周线
                    if week_time ==week_time_list[0]:
                        lastest_week_zhuzhuangtu = float(statistical_period[len(statistical_period) - 1][2]) - float(
                            statistical_period[len(statistical_period) - 1][1])
                        zui_hou_shoupanjia = float(statistical_period[i][2])
                        first_week_time = statistical_period[i][0]
                        last_five_day_price_sum = 0
                        for lastweek in range(4, 9):
                            last_five_day_price_sum = last_five_day_price_sum + float(statistical_period[lastweek][2])
                        last_five_day_price = last_five_day_price_sum / 5
                        dao_shu_di_er_zhou_shoupanjia = float(statistical_period[lastweek][2])
                        dao_shu_di_er_zhou_kaipanjia = float(statistical_period[lastweek][1])
                        dao_shu_di_er_zhou_zhuzhuangtu = float(statistical_period[lastweek][2]) - float(statistical_period[lastweek][1])
                        if zui_hou_shoupanjia > final_five_day_price and lastest_week_zhuzhuangtu > 0 and last_five_day_price > dao_shu_di_er_zhou_shoupanjia and last_five_day_price > dao_shu_di_er_zhou_kaipanjia:
                            first_week_over_flag = 1
                            continue
                        else:
                            over_week_price_flag = 0
                            break
                    else:
                        lastest_week_zhuzhuangtu = float(statistical_period[len(statistical_period) - 1][2]) - float(
                            statistical_period[len(statistical_period) - 1][1])
                        zui_hou_shoupanjia = float(statistical_period[i][2])
                        lastest_week_huanshoulv = float(statistical_period[len(statistical_period) - 1][10])
                        doushudierzhou_week_huanshoulv = float(statistical_period[len(statistical_period) - 2][10])
                        if lastest_week_zhuzhuangtu > 0 or (lastest_week_zhuzhuangtu < 0 and lastest_week_huanshoulv - doushudierzhou_week_huanshoulv < 0) and zui_hou_shoupanjia > final_five_day_price and first_week_over_flag == 1:
                            over_week_price_flag = 1
                        else:
                            over_week_price_flag = 0
                            break
            if over_week_price_flag == 1 or (len(week_time_list) == 1 and first_week_over_flag == 1):
                stock_Pressure_level_dict = self.get_stock_Pressure_level(week_statistical_period)
                atock_count_dict.update({'股票代码': atock_number})
                atock_count_dict.update({'股票名称': stock_name})
                atock_count_dict.update({'股票概念': concept})
                atock_count_dict.update({'最近1天最低价与收盘价差': (float(
                    statistical_period[len(statistical_period) - 1][2]) - float(
                    statistical_period[len(statistical_period) - 1][4])) / float(
                    statistical_period[len(statistical_period) - 2][2]) * 100})
                atock_count_dict.update({'第一交易周': first_week_time})
                atock_count_dict.update({'最后交易周': statistical_period[i][0], "最后一周涨幅": statistical_period[i][8]})
                atock_count_dict.update({'现在周涨跌幅': now_price})
                atock_count_dict.update({"压力位差率": stock_Pressure_level_dict["压力位差率"]})
                atock_count_dict.update({"支撑位差率": stock_Pressure_level_dict["支撑位差率"]})
                atock_count_dict.update({"乖离率": stock_Pressure_level_dict["乖离率"]})
                atock_count_dict.update({"最后一天涨跌幅": stock_Pressure_level_dict["最后一天涨跌幅"]})
            else:
                continue
            atock_price_margin.append(atock_count_dict)
        return atock_price_margin

    def get_stock_Pressure_level(self, statistical_period):
        """
        通过红柱和交易量计算压力位和支撑位
        """
        stock_Pressure_level={}
        zhichengweichajialv = 0
        now = statistical_period.pop()
        statistical_period.append(now)
        try:
            now_price = now[8]
        except:
            now_price = "none"
            # jiaoyiliang = 0
        dangtian_zhuzhuangtu = float(statistical_period[len(statistical_period)-1][2]) - float(statistical_period[len(statistical_period)-1][1])
        if dangtian_zhuzhuangtu == 0:
            dangtian_zhuzhuangtu = -0.5
        yalixian_jiaoyiliang = (dangtian_zhuzhuangtu) * float(statistical_period[len(statistical_period)-1][10])/abs(dangtian_zhuzhuangtu)
        # zhichengwei_jiaoyiliang = yalixian_jiaoyiliang
        dangtian_shoupanjia = float(statistical_period[len(statistical_period)-1][2])
        dangtian_chengjiaolv = float(statistical_period[len(statistical_period)-1][10])
        dangtian_zuidijia = float(statistical_period[len(statistical_period)-1][4])
        if dangtian_chengjiaolv == 0:
            dangtian_chengjiaolv = 100
        else:
            dangtian_chengjiaolv = dangtian_chengjiaolv
        for yalixian_time in range(1, 61):
            qianmian_kaipanjia = float(statistical_period[len(statistical_period)-1-yalixian_time][1])
            qianmian_shoupanjia = float(statistical_period[len(statistical_period)-1-yalixian_time][2])
            qianmian_zhuzhuangtu = qianmian_shoupanjia - qianmian_kaipanjia
            if qianmian_zhuzhuangtu == 0:
                qianmian_zhuzhuangtu = -0.5
            yalixian_jiaoyiliang = yalixian_jiaoyiliang + qianmian_zhuzhuangtu*float(statistical_period[len(statistical_period)-1-yalixian_time][10])/abs(qianmian_zhuzhuangtu)
            # if dangtian_zhuzhuangtu > 0:
            yalixian_guaililv = yalixian_jiaoyiliang / dangtian_chengjiaolv
            qianmian_zuidijia = float(statistical_period[len(statistical_period)-1-yalixian_time][4])
            qianmian_zuigaojia = float(statistical_period[len(statistical_period)-1-yalixian_time][3])

            if qianmian_zuidijia <= dangtian_shoupanjia <= qianmian_zuigaojia:
                yalixianchajialv = (qianmian_zuigaojia - dangtian_shoupanjia)/dangtian_shoupanjia*100
                zhichengweichajialv = (dangtian_shoupanjia - qianmian_zuidijia)/dangtian_shoupanjia*100
                stock_Pressure_level.update({"压力位差率": yalixianchajialv})
                stock_Pressure_level.update({"支撑位差率": zhichengweichajialv})
                stock_Pressure_level.update({"乖离率": yalixian_guaililv})
                stock_Pressure_level.update({"最后一天涨跌幅": now_price})
                break
            elif dangtian_shoupanjia <= qianmian_zuidijia:
                yalixianchajialv = (qianmian_zuidijia - dangtian_shoupanjia)/dangtian_shoupanjia*100
                zhichengweichajialv = (dangtian_shoupanjia - dangtian_zuidijia)/dangtian_shoupanjia*100
                yalixian_guaililv = -1000
                stock_Pressure_level.update({"压力位差率": yalixianchajialv})
                stock_Pressure_level.update({"支撑位差率": zhichengweichajialv})
                stock_Pressure_level.update({"乖离率": yalixian_guaililv})
                stock_Pressure_level.update({"最后一天涨跌幅": now_price})
                break
            else:
                continue
        if len(stock_Pressure_level) !=0:
            return stock_Pressure_level
        else:
            stock_Pressure_level.update({"压力位差率": "none"})
            stock_Pressure_level.update({"支撑位差率": "none"})
            stock_Pressure_level.update({"乖离率": zhichengweichajialv})
            stock_Pressure_level.update({"最后一天涨跌幅": now_price})
            return stock_Pressure_level

    def get_stock_week_up(self, zhangdiefu):
        """
        获取指定一周内涨跌幅的股票
        """
        up_n = 0
        atock_price_margin = []
        for atock in self.atock_data:
            atock_count_dict = {}
            atock_number = atock['stock_number']
            stock_name = atock['name']
            concept = atock['concept']
            klines_full = atock['week_klines'].replace('[', '').replace(']', '').split(', ')
            klines = klines_full
            b = klines[len(klines) - 1]
            # print(b)
            if len(klines) >= 10:
                statistical_period = klines[len(klines) - 10:len(klines)]
                statistical_period = Tool().spilt_str_list(statistical_period)
                    # 校验最后一天成交率
                if float(statistical_period[len(statistical_period)-1][8])>=zhangdiefu:
                    atock_count_dict.update({'股票代码': atock_number})
                    atock_count_dict.update({'股票名称': stock_name})
                    atock_count_dict.update({'股票概念': concept})
                    atock_count_dict.update({'统计周时间': statistical_period[len(statistical_period)-1][0]})
                    atock_price_margin.append(atock_count_dict)
        return atock_price_margin