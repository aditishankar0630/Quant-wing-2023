import numpy as np 
import pandas as pd 
import yfinance as yfin
# Used to grab the stock prices, with yahoo 
from pandas_datareader import data as pdr
import yfinance as yfin

from datetime import datetime 
# To visualize the results 
import matplotlib.pyplot as plt 
import seaborn

start = datetime(2023,1,1)
end = datetime(2023, 11, 15)
yfin.pdr_override()
symbols_list = ['ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJFINSV.NS', 'BHARTIARTL.NS', 'BPCL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS']
#array to store prices
symbols=[]

for ticker in symbols_list:     
    r = pdr.get_data_yahoo(ticker,  start,end)   
    # add a symbol column   
    r['Symbol'] = ticker    
    symbols.append(r)
# concatenate into df
df = pd.concat(symbols)
df = df.reset_index()
df = df[['Date', 'Close', 'Symbol']]
df.head()

df_pivot=df.pivot(index='Date', columns='Symbol', values='Close').reset_index()
df_pivot.head()
corr_df = df_pivot.corr(method='pearson')
#reset symbol as index (rather than 0-X)
corr_df.head().reset_index()
#remove date from row and column
corr_df = corr_df.iloc[1:,1:]
#del corr_df.index.name
corr_df.head(10)
#print(corr_df)
flattened_corr = corr_df.unstack().sort_values()
#print(flattened_corr)
least_correlated_stocks = flattened_corr.head(10).index.tolist()
lst_correlated = least_correlated_stocks[::2]
print(lst_correlated)
plt.figure(figsize=(13, 8))
seaborn.heatmap(corr_df, annot=True, cmap='RdYlGn')
# plt.figure()
plt.show()