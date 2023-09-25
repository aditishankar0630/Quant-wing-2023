# Quant-wing-2023
question 1&amp;2

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
#from nsepy import get_history as gh

start_date = date(2022,9,1)
end_date = date(2023,8,31)
tickers = ['TATAMOTORS.NS','DABUR.NS', 'ICICIBANK.NS','WIPRO.NS','INFY.NS']

def load_stock_data(start_date, end_date, ticker):
    df = pd.DataFrame()
    for i in range(len(ticker)):
        ticker1 = yf.Ticker(ticker[i])
        data = ticker1.history(start= start_date, 
                      end=end_date)
        print (data)
        #if i == 0:
            #df['Date'] = data['Date']
        df[str(ticker[i])] = data['Close']
    
    #print (df)
    return df

df_stock = load_stock_data(start_date, end_date, tickers)
df_nifty = yf.Ticker('^NSEI').history(start = start_date, end = end_date)['Close']
#df_nifty.rename(columns = {0:'NIFTY'}, inplace = True)
#print(df_nifty)
df_port = pd.concat([df_stock, df_nifty], axis = 1)
df_port.rename(columns={'Close':'NIFTY'},inplace=True)
#print(df_port)

plt.figure(figsize=(10, 10))
plt.subplots_adjust(hspace=0.5)
plt.suptitle("Daily closing prices", fontsize=18, y=0.95)
for n, ticker in enumerate(tickers):
    ax = plt.subplot(3, 2, n + 1)
    df_stock[ticker].plot(ax= ax)
    ax.set_title(ticker.upper())
plt.show()

df_returns = df_port.pct_change().dropna().reset_index()
plt.figure(figsize=(10, 10))
plt.subplots_adjust(hspace=0.5)
plt.suptitle("Daily Returns", fontsize=18, y=0.95)
for n, ticker in enumerate(tickers):
    ax = plt.subplot(3, 2, n + 1)    
    df_returns[ticker].plot(ax= ax)       
    ax.set_title(ticker.upper())
plt.show()

beta = []
alpha = []

for i in df_returns.columns:
  if i != 'Date' and i != 'NIFTY':
    df_returns.plot(kind = 'scatter', x = 'NIFTY', y = i)
    b, a = np.polyfit(df_returns['NIFTY'], df_returns[i], 1)
    plt.plot(df_returns['NIFTY'], b * df_returns['NIFTY'] + a, '-', 
                            color = 'r')  
    beta.append(b)    
    alpha.append(a) 
print(beta)
#plt.show()

ER = []
rf = 0.06 
rm = df_returns['NIFTY'].mean() * 252
print(f'Market return is {rm}%')

for i in beta:
  ER_tmp = rf + (i * (rm-rf)) 
  ER.append(ER_tmp)
  print(f'Expected return based on CAPM for {tickers[i]} is  {ER_tmp}')

portfolio_weights = 1/len(tickers) * np.ones(len(tickers)) 
ER_portfolio = sum(ER * portfolio_weights)
print(f'Portfolio expected return is {round(ER_portfolio,2)} %')
    
