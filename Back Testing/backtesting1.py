import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sns
plt.style.use('seaborn-v0_8')
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf

ticker = yf.Ticker('AAPL')
df = ticker.history(start='2004-01-01', end='2024-07-08').round(2)
df.columns = df.columns.str.lower()
print(df.head())

df['sma1'] = df['close'].rolling(window=20).mean()
df['sma2'] = df['close'].rolling(window=120).mean()

df['signal'] = 0
df.loc[df['sma1'] > df['sma2'], 'signal'] = 1
df.loc[df['sma1'] < df['sma2'], 'signal'] = -1

df[['close','sma1','sma2']][2200:].plot(figsize=(12,6))
plt.show()
# 生成信號
signal = np.zeros([len(df)])
condition1 = (df['sma1']>df['sma2'])
condition2 = (df['sma1']<df['sma2'])
# 
for i in range(len(df)):
    if condition1[i] :
        signal[i] = 1
    elif condition2[i] :
        signal[i] = -1
signal_df = pd.Series(signal,index = df.index)
plt.figure(figsize=(12,6))
signal_df[:500].plot()
plt.show()

position_df=signal_df.shift(1)
position_df.plot(figsize=(12,6))
plt.show()

df['position'] = position_df
df = df[['close','sma1','sma2','position']].dropna()
print(df.head())

df['ret'] = df['close'].pct_change()
df['cum_ret'] = df['ret'].cumsum()

# 兩種算法，前者可針對不同報酬如借券利息等細部計算
strategy_ret = np.zeros(len(df))
for i in range(len(df)):
    if df['position'][i] == 1:
        strategy_ret[i] = df['ret'][i]*df['position'][i]
    elif df['position'][i] == -1 :
        strategy_ret[i] = df['ret'][i]*df['position'][i]
strategy_ret = df['ret']*df['position']
df['strategy_ret'] = strategy_ret
df['cum_strategy_ret'] = df['strategy_ret'].cumsum()

## 比較單獨持有和執行策略的損益
fig,ax=plt.subplots(figsize=(16,6))
df[['cum_strategy_ret','cum_ret']].plot(label='Total Return',ax=ax)
plt.legend()
plt.title('Stock & Total Return',fontsize=16)
plt.show()

## 建累機報酬率的df
## 並且以.cummax()來計算累積報酬創高點


fig=plt.figure(figsize=(16,6))
plt.subplot(1,2,1)
df['cum_strategy_ret'].cummax().plot()
plt.title('Cummax Return')
plt.subplot(1,2,2)
df['cum_strategy_ret'].plot()
plt.title('Cumulative Return')
plt.show()

MDD_series=df['cum_strategy_ret'].cummax()-df['cum_strategy_ret']
MDD_series.plot()
high_index = df['cum_strategy_ret'][df['cum_strategy_ret'].cummax()==df['cum_strategy_ret']].index
print(high_index)
fig,ax=plt.subplots(figsize=(16,6))
df['cum_strategy_ret'].plot(label='Total Return',ax=ax,c='r')
plt.fill_between(MDD_series.index,-MDD_series,0,facecolor='r',label='DD')
plt.scatter(high_index,df['cum_strategy_ret'].loc[high_index],c='#02ff0f',label='High')
plt.legend()
plt.ylabel('Return%')
plt.xlabel('Date')
plt.title('Return & MDD',fontsize=16);
plt.show()

MDD=round(MDD_series.max(),2)*100
Cumulative_Return=round(df['cum_strategy_ret'].iloc[-1],2)*100
Return_on_MDD=round(df['cum_strategy_ret'].iloc[-1]/MDD_series.max(),2)
daily_return=df['cum_strategy_ret'].diff(1)

print('Cumulative Return: {}%'.format(Cumulative_Return))
print('MDD: {}%'.format(MDD))
print('Return on MDD: {}'.format(Return_on_MDD))
print('Shapre Ratio: {}'.format(round((daily_return.mean()/daily_return.std())*pow(252,0.5),2)))