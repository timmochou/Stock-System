import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sns
plt.style.use('seaborn-v0_8')
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf

## 設定變數
start_day = '2010-01-01'
end_day = datetime.today().strftime('%Y-%m-%d')

company_list = ['麗正', '聯電', '華泰', '台積電', '旺宏']
code_list = ['2302', '2303', '2329', '2330', '2337']

# 讀入data
stock_data = {}
for company, code in zip(company_list, code_list):
    try:
        print(f'正在下載 {company} ({code}) 的數據...')
        ticker = yf.Ticker(f'{code}.TW')
        stock_data[company] = ticker.history(start=start_day, end=end_day)
        print(f'{company} 數據下載成功')
    except Exception as e:
        print(f'下載 {company} 數據時發生錯誤: {str(e)}')

print('全部下載完成')
print(stock_data['麗正'].head())


## 組合adj close df
adj_close_list = []
for company in company_list:
    adj_close_list.append(stock_data[company]['Close'])
close_df = pd.concat(adj_close_list, axis=1, keys=code_list, join='inner')
close_df.tail()

print(close_df.info())
# 查看平均
print(close_df.describe())


# plot the data 
# plt.figure(figsize=(10, 12))
# for col in close_df:
#     plt.subplot(5, 1, close_df.columns.to_list().index(col)+1)
#     plt.title(col)
#     close_df[col].plot()
# plt.tight_layout()
# plt.show()


plt.figure(figsize=(9,7.5))
plt.title('Correlation Matrix')
sns.heatmap(close_df.corr(),annot=True,annot_kws={"size":15},cmap='coolwarm')
plt.show()

# 計算日收益率
returns_df = close_df.pct_change()

# 對收益率進行 ADF 測試
for column in returns_df.columns:
    result = adfuller(returns_df[column].dropna())
    print(f'\n{column} 收益率的 ADF 測試結果:')
    print(f'ADF 統計量: {result[0]:.4f}')
    print(f'p-value: {result[1]:.4f}')

# plot the data with pct_change
plt.figure(figsize=(6,10))
for col in close_df:
    plt.subplot(5,1,close_df.columns.to_list().index(col)+1)
    plt.title(col)
    close_df[col].pct_change(periods=1,fill_method="ffill").plot()
plt.tight_layout()
plt.show()

## 解決trend，做一階差分

plt.figure(figsize=(9,7.5))
plt.title('Correlation Matrix');
sns.heatmap(close_df.pct_change(periods=1,fill_method="ffill").corr(),annot=True,annot_kws={"size":15},cmap='coolwarm')
plt.show()
# 計算對數收益率
# 公式：ln(P_t / P_t-1)，其中 P_t 是 t 時刻的價格
# 在金融分析中優先使用對數收益率的原因：
# 1. 具有時間可加性
# 2. 更接近常態分布
# 3. 在模擬中可以避免股票價格出現負值
rets = np.log(close_df/close_df.shift(1))
print(rets.head().round(2))
# plot the cumulative return

rets.cumsum().apply(np.exp).plot(figsize=(12,6))
plt.show()
# 計算5日移動平均
for i in close_df.columns:
    close_df['{} sma1'.format(i)]=close_df[i].rolling(5).mean()
print(close_df.head())
# 計算20日min,max,mean,std,median,ewma
df = pd.DataFrame(close_df['2330'])
print(df.describe())
df['20_min'] = df['2330'].rolling(20).min()
df['20_max'] = df['2330'].rolling(20).max()
df['20_mean'] = df['2330'].rolling(20).mean()
df['20_std'] = df['2330'].rolling(20).std()
df['20_median'] = df['2330'].rolling(20).median()
df['20_ewma'] = df['2330'].ewm(halflife = 0.5,min_periods = 20).mean()
print(df.head())


