from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pymysql
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
            url = f"https://tw.stock.yahoo.com/quote/{symbol}/profile"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            
            company_name = soup.find('h1', {'class':'C($c-link-text) Fw(b) Fz(24px) Mend(8px)'}).getText()
            company_code = soup.find('span', {'class':'C($c-icon) Fz(24px) Mend(20px)'}).getText()
            data_date = soup.find('span', {'class':'Fz(14px) C(#5b636a)'}).getText()
            # 先轉換為 datetime 對象，然後再轉換為所需的字符串格式
            data_date = datetime.strptime(data_date.split('：')[1].strip(), '%Y/%m/%d').strftime('%Y/%m/%d')
            info_elements = soup.find_all('div', {'class' : 'Py(8px) Pstart(12px) Bxz(bb)'})

            # 根據順序獲取各項資訊
            establish_date = info_elements[6].getText() #成立日期
            industry_category = info_elements[8].getText()  #產業類別
            Chairman = info_elements[10].getText() #董事長
            share_capital = info_elements[14].getText() #股本
            Issued_Common_Shares = info_elements[16].getText() #流通股數
            Market_Capital = info_elements[18].getText() #市值
            mkt_type = info_elements[19].getText() #上市資訊
            Dir_Super_Ratio_hold = info_elements[20].getText() #大股東持股比例
            company_info.append((data_date, company_code, company_name, establish_date, industry_category, Chairman, share_capital, Issued_Common_Shares, Market_Capital, mkt_type, Dir_Super_Ratio_hold))

        return company_info

    def get_data(self):
        return {}

    def save_data(self, company_info):
        db_settings = {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "Tim27821901",
            "db": "STOCK",
            "charset": "utf8"
        }
        conn = None  # 初始化連接變數
        try:
            conn = pymysql.connect(**db_settings)
            with conn.cursor() as cursor:
                for company in company_info:
                    sql = "INSERT INTO FACT_COMPANY_INFO (data_date, company_code, company_name, establish_date, industry_category, Chairman, share_capital, Issued_Common_Shares, Market_Capital, mkt_type, Dir_Super_Ratio_hold) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, company)
                conn.commit()
        except Exception as ex:
            print("Exception:", ex)
        finally:
            if conn:  # 確保資料庫連接被正確關閉
                conn.close()

stocks = Company('6768.TW', '6919.TW', '8937.TW', '2615.TW', '4958.TW') # 可以加入任意數量的股票代號
stocks.save_data(stocks.get_name())

