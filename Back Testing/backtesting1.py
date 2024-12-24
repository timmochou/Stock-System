import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sns
plt.style.use('seaborn-v0_8')
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf

# 獲取股票數據
ticker = yf.Ticker('AAPL')
df = ticker.history(start='2004-01-01', end='2024-07-08').round(2)
df.columns = df.columns.str.lower()
print(df.head())

# 計算技術指標
df['sma1'] = df['close'].rolling(window=20).mean()
df['sma2'] = df['close'].rolling(window=120).mean()

# 生成交易信號
df['signal'] = 0
df.loc[df['sma1'] > df['sma2'], 'signal'] = 1
df.loc[df['sma1'] < df['sma2'], 'signal'] = -1

df[['close','sma1','sma2']][2200:].plot(figsize=(12,6))
plt.show()

# 使用另一種方式生成信號
signal = np.zeros([len(df)])
condition1 = (df['sma1']>df['sma2'])
condition2 = (df['sma1']<df['sma2'])

# 遍歷生成信號
for i in range(len(df)):
    if condition1[i]:
        signal[i] = 1
    elif condition2[i]:
        signal[i] = -1

# 創建持倉序列
position_df = signal_df.shift(1)
position_df.plot(figsize=(12,6))
plt.show()

df['position'] = position_df
df = df[['close','sma1','sma2','position']].dropna()
print(df.head())

# 計算收益率
df['ret'] = df['close'].pct_change()
df['cum_ret'] = df['ret'].cumsum()

# 計算策略收益
strategy_ret = np.zeros(len(df))
for i in range(len(df)):
    if df['position'][i] == 1:
        strategy_ret[i] = df['ret'][i]*df['position'][i]
    elif df['position'][i] == -1:
        strategy_ret[i] = df['ret'][i]*df['position'][i]

# 計算最大回撤相關指標
MDD_series = df['cum_strategy_ret'].cummax() - df['cum_strategy_ret']
high_index = df['cum_strategy_ret'][df['cum_strategy_ret'].cummax()==df['cum_strategy_ret']].index

# 計算績效指標
MDD = round(MDD_series.max(),2)*100
Cumulative_Return = round(df['cum_strategy_ret'].iloc[-1],2)*100
Return_on_MDD = round(df['cum_strategy_ret'].iloc[-1]/MDD_series.max(),2)
daily_return = df['cum_strategy_ret'].diff(1)

# 計算夏普比率：年化收益率/年化波動率，其中252為交易日數
Sharpe_Ratio = round((daily_return.mean()/daily_return.std())*pow(252,0.5),2)

print('Cumulative Return: {}%'.format(Cumulative_Return))
print('MDD: {}%'.format(MDD))
print('Return on MDD: {}'.format(Return_on_MDD))
print('Shapre Ratio: {}'.format(Sharpe_Ratio))