# coding=utf-8
import time

import requests
from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup


class tonghuashun_cashflow_html(object):

    def get_html(self, cookie, page):
        """
        获取概念涨跌数据
        cookie：登录https://data.10jqka.com.cn/funds/gnzjl/field/tradezdf/order/desc/page/1/ajax/1/free/1/
        """
        web_url = 'https://data.10jqka.com.cn/funds/gnzjl/field/tradezdf/order/desc/page/%d/ajax/1/free/1/' % page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cookie': cookie}  # 给请求指定一个请求头来模拟chrome浏览器
        r = requests.get(web_url, headers=headers)  # 像目标url地址发送get请求，返回一个response对象
        soup = BeautifulSoup(r.content.decode("gbk"), 'lxml')
        return soup

    def get_cookies(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=options,
                                  executable_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe')
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                               Object.defineProperty(navigator, 'webdriver', {
                                 get: () => undefined
                               })
                             """
        })
        driver.get(
            "https://data.10jqka.com.cn/funds/gnzjl/field/tradezdf/order/desc/page/2/ajax/1/free/1/")
        # for c in cookiestr.keys():
        #    driver.add_cookie({'name':c,'value':cookiestr[c]})

        cookie = driver.get_cookies()
        cookies = cookie[0]['name'] + '=' + cookie[0]['value']
        driver.close()
        return cookies

    def get_concept_data(self, html):
        """
        获取股票产品信息列表
        """
        record_list = []
        table = html.select('.J-ajax-table')[0]
        tbody = table.select('tbody tr')
        # 当tbody为空时，则说明当前页已经没有数据了，此时终止循环
        if len(tbody) == 0:
            print('tbody is none')
        else:
            for tr in tbody:
                fields = tr.select('td')
                record = [field.text.strip() for field in fields[1:]]
                record2 = fields[1].next['href']
                record_list.append(record)
            print(record)
            return record_list

    def get_concept_record(self):
        concept_record_list = []
        for i in range(1, 6):
            cookies = self.get_cookies()
            html = self.get_html(cookies, i)
            concept_record = self.get_concept_data(html)
            concept_record_list.extend(concept_record)
            time.sleep(2)
        return concept_record_list


    def get_concept_list_element(self):
        """
        获取股票涉及概念列表
        """
        concept_list_element = self.html.xpath('/html/body/table/tbody/tr/td[6]/div/descendant::a')
        concept_str = ""
        for i in concept_list_element:
            if i.text != '更多':
                concept_str = concept_str + ',' + i.text
            if len(concept_str) > 255:
                concept_str = '异常：超字段长度'
        return concept_str

    def get_city_element(self):
        """
        获取股票所属城市
        """
        city_element = self.html.xpath('/html/body/table/tbody/tr/td[4]/div/descendant::a')
        city_str = ""
        for i in city_element:
            if i.text != '更多':
                city_str = city_str + ',' + i.text
            if len(city_str) > 64:
                city_str = '异常：超字段长度'
        return city_str

    def get_ndustry_element(self):
        """
        获取股票所属行业
        """
        ndustry_element = self.html.xpath('/html/body/table/tbody/tr/td[3]/div/descendant::a')
        ndustry_str = ""
        for i in ndustry_element:
            if i.text != '更多':
                ndustry_str = ndustry_str + ',' + i.text
            if len(ndustry_str) > 64:
                ndustry_str = '异常：超字段长度'
        return ndustry_str


if __name__ == '__main__':
    tonghuashun_cashflow_html().get_concept_record()



