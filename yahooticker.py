import yfinance as yf
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from math import floor
from termcolor import colored as cl 

sym = 'SBIN.NS'
startdt = '2023-08-01'
def get_historical_data(symbol, start_date = None):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(start=start_date)
    return hist
data = get_historical_data(str(sym),startdt)
#print(data)

def get_rsi(close, lookback):
    ret = close.diff()
    up = []
    down = []
    for i in range(len(ret)):
        if ret[i] < 0:
            up.append(0)
            down.append(ret[i])
        else:
            up.append(ret[i])
            down.append(0)
    up_series = pd.Series(up)
    down_series = pd.Series(down).abs()
    up_ewm = up_series.ewm(com = lookback - 1, adjust = False).mean()
    down_ewm = down_series.ewm(com = lookback - 1, adjust = False).mean()
    rs = up_ewm/down_ewm
    rsi = 100 - (100 / (1 + rs))
    rsi_df = pd.DataFrame(rsi).rename(columns = {0:'rsi'}).set_index(close.index)
    rsi_df = rsi_df.dropna()
    return rsi_df[3:]

data['rsi_14'] = get_rsi(data['Close'], 14)
data = data.dropna()
#print(data)

# ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
# ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)
# ax1.plot(data['Close'], linewidth = 2.5)
# ax1.set_title(str(sym) + ' CLOSE PRICE')
# ax2.plot(data['rsi_14'], color = 'orange', linewidth = 2.5)
# ax2.axhline(30, linestyle = '--', linewidth = 1.5, color = 'grey')
# ax2.axhline(70, linestyle = '--', linewidth = 1.5, color = 'grey')
# ax2.set_title(str(sym) + ' RELATIVE STRENGTH INDEX')
# plt.show()

def implement_rsi_strategy(prices, rsi):    
    buy_price = []
    sell_price = []
    rsi_signal = []
    signal = 0

    for i in range(len(rsi)):
        if rsi[i-1] > 30 and rsi[i] < 30:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                rsi_signal.append(0)
        elif rsi[i-1] < 70 and rsi[i] > 70:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                rsi_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            rsi_signal.append(0)
            
    return buy_price, sell_price, rsi_signal
            

buy_price, sell_price, rsi_signal = implement_rsi_strategy(data['Close'], data['rsi_14'])

# ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
# ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)
# ax1.plot(data['Close'], linewidth = 2.5, color = 'skyblue', label = str(sym))
# ax1.plot(data.index, buy_price, marker = '^', markersize = 10, color = 'green', label = 'BUY SIGNAL')
# ax1.plot(data.index, sell_price, marker = 'v', markersize = 10, color = 'r', label = 'SELL SIGNAL')
# ax1.set_title(str(sym) + ' RSI TRADE SIGNALS')
# ax2.plot(data['rsi_14'], color = 'orange', linewidth = 2.5)
# ax2.axhline(30, linestyle = '--', linewidth = 1.5, color = 'grey')
# ax2.axhline(70, linestyle = '--', linewidth = 1.5, color = 'grey')
# plt.show()

position = []
for i in range(len(rsi_signal)):
    if rsi_signal[i] > 1:
        position.append(0)
    else:
        position.append(1)
        
for i in range(len(data['Close'])):
    if rsi_signal[i] == 1:
        position[i] = 1
    elif rsi_signal[i] == -1:
        position[i] = 0
    else:
        position[i] = position[i-1]
        
rsi = data['rsi_14']
close_price = data['Close']
rsi_signal = pd.DataFrame(rsi_signal).rename(columns = {0:'rsi_signal'}).set_index(data.index)
position = pd.DataFrame(position).rename(columns = {0:'rsi_position'}).set_index(data.index)

frames = [close_price, rsi, rsi_signal, position]
strategy = pd.concat(frames, join = 'inner', axis = 1)

#print(strategy.head())

data_ret = pd.DataFrame(np.diff(data['Close'])).rename(columns = {0:'returns'})
rsi_strategy_ret = []

for i in range(len(data_ret)):
    returns = data_ret['returns'][i]*strategy['rsi_position'][i]
    rsi_strategy_ret.append(returns)
    
rsi_strategy_ret_df = pd.DataFrame(rsi_strategy_ret).rename(columns = {0:'rsi_returns'})
investment_value = 100000
number_of_stocks = floor(investment_value/data['Close'][-1])
rsi_investment_ret = []

for i in range(len(rsi_strategy_ret_df['rsi_returns'])):
    returns = number_of_stocks*rsi_strategy_ret_df['rsi_returns'][i]
    rsi_investment_ret.append(returns)

rsi_investment_ret_df = pd.DataFrame(rsi_investment_ret).rename(columns = {0:'investment_returns'})
total_investment_ret = round(sum(rsi_investment_ret_df['investment_returns']), 2)
profit_percentage = floor((total_investment_ret/investment_value)*100)
print (rsi_investment_ret_df.loc[(rsi_investment_ret_df['investment_returns'] != 0)])
print(cl('Profit gained from the RSI strategy by investing ' + str(investment_value) + ' in ' + str(sym) + ' : {}'.format(total_investment_ret), attrs = ['bold']))
print(cl('Profit percentage of the RSI strategy : {}%'.format(profit_percentage), attrs = ['bold']))

def yahoofinmetohds():
    msft = yf.Ticker("SBIN.NS")

    yf.version

    # get all stock info
    print(msft.info)

    # get historical market data
    hist = msft.history(period="1mo")
    print (hist)

    # show meta information about the history (requires history() to be called first)
    print(msft.history_metadata)

    # show actions (dividends, splits, capital gains)
    msft.actions
    msft.dividends
    msft.splits
    msft.capital_gains  # only for mutual funds & etfs

    # show share count
    msft.get_shares_full(start="2022-01-01", end=None)

    # show financials:
    # - income statement
    msft.income_stmt
    msft.quarterly_income_stmt
    # - balance sheet
    msft.balance_sheet
    msft.quarterly_balance_sheet
    # - cash flow statement
    msft.cashflow
    msft.quarterly_cashflow
    # see `Ticker.get_income_stmt()` for more options

    # show holders
    msft.major_holders
    msft.institutional_holders
    msft.mutualfund_holders

    # Show future and historic earnings dates, returns at most next 4 quarters and last 8 quarters by default. 
    # Note: If more are needed use msft.get_earnings_dates(limit=XX) with increased limit argument.
    msft.earnings_dates

    # show ISIN code - *experimental*
    # ISIN = International Securities Identification Number
    msft.isin

    # show options expirations
    msft.options

    # show news
    msft.news

    # get option chain for specific expiration
    #opt = msft.option_chain('2023-09-01')
    # data available via: opt.calls, opt.puts
