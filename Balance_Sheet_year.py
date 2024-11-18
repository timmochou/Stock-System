from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pymysql
from lxml import html
class Company:
    # 初始化
    # symbol: 股票代號
    # name: 股票名稱
    def __init__(self, *symbols):
        self.symbols = symbols     # 保存為元組
        # self.name = self.get_name()   # 獲取並保存股票名稱
        # self.data = self.get_data()   # 獲取並保存股票數據

    # 獲取股票名稱
    def get_name(self):
        company_info = list() # 儲存股票資訊

        for symbol in self.symbols:
            url = f"https://www.cmoney.tw/finance/{symbol}/f00040?o=3"
            response = requests.get(url)
            print(response.text)  # 打印响应内容以调试
            
            # 使用 lxml 解析 HTML
            tree = html.fromstring(response.content)

            company_name = tree.xpath('//h2[@class="page-title"]/text()')[0].split('(')[0]
            company_code = tree.xpath('//h2[@class="page-title"]/text()')[0].split('(')[1].split(')')[0]
            
            # 使用 XPath 查找时间元素
            time_element = tree.xpath('//*[@id="HeaderContent"]/time')
            if time_element:
                data_date = time_element[0].xpath('span[2]/text()')[0]  # 获取第二个 span 的文本
            else:
                data_date = "未找到日期"  # 或者处理为其他默认值
            
            company_info.append((company_name, company_code, data_date))
            
        return company_info

    def get_data(self):
        return {}


stocks = Company('6768', '6919', '8937', '2615', '4958') # 可以加入任意數量的股票代號
print(stocks.get_name())
