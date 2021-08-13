# coding=utf-8
import json
import requests
from lxml import etree
from selenium import webdriver


class HtmlDataGet(object):

    def __init__(self, stock_number, cookie):
        """
        获取股票行业、概念信息
        stock_number：股票代码
        cookie：登录http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=600862
        """
        headers = {
            'Host': 'www.iwencai.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': cookie}  #给请求指定一个请求头来模拟chrome浏览器
        payload = {
                    'pid': '8153',
                    'codes': stock_number,
                    'codeType': 'stock',
                    'info': '{"view":{"nolazy":1,"parseArr":{"_v":"new","dateRange":[],"staying":[],"queryCompare":[],"comparesOfIndex":[]},"asyncParams":{"tid":137}}}'}
        web_url = 'http://www.iwencai.com/diag/block-detail'
        r = requests.get(web_url, headers=headers, params=payload) #像目标url地址发送get请求，返回一个response对象
        content = str(r.content.decode())
        if content.find('Nginx forbidden') != -1:
            cookie = self.get_cookies(stock_number)
            headers = {
                'Host': 'www.iwencai.com',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'DNT': '1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cookie': cookie}  # 给请求指定一个请求头来模拟chrome浏览器
            r = requests.get(web_url, headers=headers, params=payload)  # 像目标url地址发送get请求，返回一个response对象
            content = str(r.content.decode())
        try:
            table_dict = json.loads(content)['data']['data']['tableTempl'].replace("\n", "")
        except Exception as e:
            print(e)
            table_dict = '<table border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:788px;\">\n<thead>\n<tr>\n<th>\n<span\n                                    class=\"th_words\">股票代码</span></th>\n<th>\n<span\n                                    class=\"th_words\">股票简称</span></th>\n<th>\n<span\n                                    class=\"th_words\">所属行业</span></th>\n<th>\n<span\n                                    class=\"th_words\">城市</span></th>\n<th>\n<span\n                                    class=\"th_words\">主营产品名称</span></th>\n<th>\n<span\n                                    class=\"th_words\">所属概念</span></th>\n</tr>\n</thead>\n<tbody>\n<tr class=\"even_row\">\n<td width=\"66\" colnum=\"0\"\n                            class=\"item\">\n<div class=\"em\">000506</div>\n</td>\n<td width=\"67\" colnum=\"1\"\n                            class=\"item\">\n<div class=\"em alignCenter graph\"><a target=\"_blank\" href=\"/stockpick/search?tid=stockpick&qs=stockpick_diag&ts=1&w=000506\">中润资源</a></div>\n</td>\n<td width=\"91\" colnum=\"2\"\n                            class=\"item\">\n<div class=\"em\"><a target=\"_blank\" href=\"http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E5%90%8C%E8%8A%B1%E9%A1%BA%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E5%8C%85%E5%90%AB%E6%9C%89%E8%89%B2%E5%86%B6%E7%82%BC%E5%8A%A0%E5%B7%A5\">异常1</a></div>\n</td>\n<td width=\"55\" colnum=\"3\"\n                            class=\"item\">\n<div class=\"em alignLeft\"><a target=\"_blank\" href=\"/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E5%9F%8E%E5%B8%82%E4%B8%BA%E6%B5%8E%E5%8D%97%E5%B8%82\" substr=\"济南市\" fullstr=\"济南市\" title=\"济南市\">济南市</a></div>\n</td>\n<td width=\"201\" colnum=\"4\"\n                            class=\"item sortCol\">\n<div class=\"em split\"><a href=\"\" class=\"ml5 moreSplit fr\" num=\"1\">异常1</a><span class=\"fl\">【<a target=\"_blank\" href=\"/stockpick/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%88%BF%E5%9C%B0%E4%BA%A7\">异常1</a>】;</span><span class=\"fl\">【<a target=\"_blank\" href=\"/stockpick/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E5%95%86%E5%93%81%E6%88%BF\">异常1</a>】;</span><span class=\"fl hidden\">【<a target=\"_blank\" href=\"/stockpick/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E4%BD%8F%E5%AE%85%E5%9C%B0%E4%BA%A7\">异常1</a>】;</span><span class=\"fl hidden\">【<a target=\"_blank\" href=\"/stockpick/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%88%BF%E5%9C%B0%E4%BA%A7%E4%B8%9A%E5%8A%A1\">异常1</a>】;</span><span class=\"fl hidden\">【<a target=\"_blank\" href=\"/stockpick/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E9%93%81%E7%9F%BF\">异常1</a>】</span></div>\n</td>\n<td width=\"223\" colnum=\"5\"\n                            class=\"item\">\n<div class=\"em alignCenter split\"><span class=\"fl\"><a target=\"_blank\" href=\"/stockpick/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E6%B6%89%E7%9F%BF\">异常1</a> ;</span><span class=\"fl\"><a target=\"_blank\" href=\"/stockpick/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E9%BB%84%E9%87%91%E6%A6%82%E5%BF%B5\">异常1</a> ;</span><span class=\"fl\"><a target=\"_blank\" href=\"/stockpick/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E8%9E%8D%E8%B5%84%E8%9E%8D%E5%88%B8\">异常1</a> ;</span><span class=\"fl\"><a target=\"_blank\" href=\"/stockpick/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E8%BD%AC%E8%9E%8D%E5%88%B8%E6%A0%87%E7%9A%84\">异常1</a>\n</span></div>\n</td>\n</tr>\n</tbody>\n</table>'
            pass
        table_element = table_dict
        self.html = etree.HTML(table_element)

    def get_cookies(self, stock_number):
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
            "http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w="+ str(stock_number))
        # for c in cookiestr.keys():
        #    driver.add_cookie({'name':c,'value':cookiestr[c]})

        cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
        cookie_dict = {}
        for i in cookie:
            split_list = i.split('=')
            cookie_dict.update({split_list[0]: split_list[1]})
        cookie_str = 'cid' + '=' + cookie_dict['cid'] + '; ' + 'ComputerID' + '=' + cookie_dict[
            'ComputerID'] + '; ' + 'WafStatus' + '=' + cookie_dict[
                         'WafStatus'] + '; ' + 'other_uid' + '=' + 'Ths_iwencai_Xuangu_bgee9foa6zwk1ksuqxbxbxdhwp5f26th' + '; ' + 'ta_random_userid' + '=' + 'xgwoi1enwi' + '; ' + 'PHPSESSID' + '=' + cookie_dict['PHPSESSID'] + '; ' + 'v' + '=' + \
                     cookie_dict['v'] + '; '
        # cookiestr = ';'.join(item for item in cookie)
        driver.close()
        return cookie_str

    def get_product_list_element(self):
        """
        获取股票产品信息列表
        """
        product_str = ""
        product_list_element = self.html.xpath('/html/body/table/tbody/tr/td[5]/div/descendant::a')
        for i in product_list_element:
            if i.text != '更多':
                product_str = product_str + ',' + i.text
            if len(product_str) >1000:
                product_str = '异常：超字段长度'
        return product_str

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
    b = 'cid=766ed7fe98a999d244492640a07298ba1626454288; ComputerID=766ed7fe98a999d244492640a07298ba1626454288; WafStatus=0; other_uid=Ths_iwencai_Xuangu_bgee9foa6zwk1ksuqxbxbxdhwp5f26th; PHPSESSID=cea51b4cce8c1140db3c49fa7b28e28a; v=A2LmD72Ld76QsGviBM6Cog1es-PHs2e_GLRa8az6jJKALAwVlEO23ehHqlF_'
    a = HtmlDataGet(603838, b)
    print(a.get_city_element())

