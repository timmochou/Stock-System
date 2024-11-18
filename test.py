import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties  # 新增字體設定
from datetime import datetime  # 新增這行

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 用來正確顯示負號

# 下載數據
now = datetime.now().strftime('%Y-%m-%d')  # 獲取今天日期
twii = yf.download("6768.TW", start="2023-01-01", end=now)
twii['Close'].plot()
plt.title('志強-KY')
plt.ylabel('價格')
plt.grid(True)
plt.show()