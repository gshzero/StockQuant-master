import pymysql


host = 'localhost'
port = 3306
db = 'atock'
user = 'root'
password = '13549812386'


# ---- 用pymysql 操作数据库
def get_connection():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn


def check_it():

    conn = get_connection()

    # 使用 cursor() 方法创建一个 dict 格式的游标对象 cursor
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("select stock_number,name,klines from stock_klines")

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    # conn = get_connection()
    #
    # # 使用 cursor() 方法创建一个 dict 格式的游标对象 cursor
    # cursor2 = conn.cursor(pymysql.cursors.DictCursor)
    #
    # # 使用 execute()  方法执行 SQL 查询
    # for i in data:
    #   sql = "INSERT INTO stock_list (stock_number, stock_name) VALUES ( %s, %s);" % ("\"" + i['stock_number'] + "\"", "\"" + i['name'] + "\"")
    #   print(sql)
    #   cursor2.execute(sql)
    #
    # print("完成导入")
    #
    # # 关闭数据库连接
    # cursor.close()
    # conn.close()

def get_cookies():
    from selenium import webdriver

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options, executable_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe')
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                          get: () => undefined
                        })
                      """
    })
    driver.get("http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=600862")
    # for c in cookiestr.keys():
    #    driver.add_cookie({'name':c,'value':cookiestr[c]})

    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookie_dict = {}
    for i in cookie:
        split_list = i.split('=')
        cookie_dict.update({split_list[0]:split_list[1]})
    cookie_str = 'cid' + '=' + cookie_dict['cid']+'; ' + 'ComputerID' + '=' + cookie_dict['ComputerID'] + '; ' + 'WafStatus' + '=' + cookie_dict['WafStatus']+'; ' + 'other_uid' + '=' + 'Ths_iwencai_Xuangu_bgee9foa6zwk1ksuqxbxbxdhwp5f26th' + '; ' + 'ta_random_userid' + '=' + 'xgwoi1enwi' + '; ' + 'vvvv' + '=' + cookie_dict['vvvv']+'; ' + 'PHPSESSID' + '=' + cookie_dict['PHPSESSID']+'; '+ 'v' + '=' + cookie_dict['v']+'; '
    # cookiestr = ';'.join(item for item in cookie)
    driver.close()
    return cookie_str

def get_list():
    c = []
    a = ["'2021-08-05,3.10,3.09,3.16,3.08,247864,77139292.00,2.57,-0.64,-0.02,0.99'", "'2021-08-06,3.08,3.07,3.09,3.04,174779,53361342.00,1.62,-0.65,-0.02,0.70'", "'2021-08-09,3.06,3.08,3.09,3.05,160322,49308970.00,1.30,0.33,0.01,0.64'", "'2021-08-10,3.08,3.11,3.12,3.07,175021,54338679.00,1.62,0.97,0.03,0.70'"]
    for i  in a:
        i = i.replace("\'","")
        b = i.split(',')
        c.append(b)
    print(c)
    print(c[0][0])

if __name__ == '__main__':
    # a = 2
    # print(pow(a, 1.1))
    # dict= {}
    # b = [1,2,3]
    # dict.update({'l':b})
    # print(dict)
    get_list()
    # check_it()