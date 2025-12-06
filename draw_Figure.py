import matplotlib.pyplot as plt
import matplotlib
import mplfinance as mpf
import yfinance as yf
from curl_cffi import requests
test1

# plt.rcParams['font.family'] = 'Microsoft JhengHei'
matplotlib.rc('font', family='Microsoft JhengHei')
session = requests.Session(impersonate="chrome")

def draw_fig(search_stock, period, ticker):
    
    diff, diff_ratio, yes_price = calculate_increase_decrease(search_stock, period, ticker)
    last_price = ticker['Close'].iloc[-1] # 今日收盤/最新收盤
    
    ticker['Datetime'] = ticker.index.strftime('%Y-%m-%d %H:%M:%S')
    # Fig1
    '''
    fig, ax1 = plt.subplots()

    if period in ['1d', '5d', '1mo', '6mo']:
        # 直方圖在左邊 Y 軸
        ax1.plot(ticker.index, ticker['Close'], color='red', marker=None)
        ax1.set_ylabel('股價')
        # 折線圖在右邊 Y 軸
        ax2 = ax1.twinx()
        ax2.bar(ticker.index, ticker['Volume'], color='lightgreen', width=0.001, alpha=0.5)
        ax2.set_ylabel('成交量')
    else:
        ax1.plot(ticker.index, ticker['Close'], color='red', marker=None)
        ax1.set_ylabel('股價')
    
    last_price = ticker['Close'].iloc[-1] # 今日收盤/最新收盤
    first_price = ticker['Close'].iloc[0] # 前日收盤/起始點收盤
    diff = last_price - first_price
    diff_ratio = diff / first_price
    fig.suptitle(f"{search_stock}\n現價：{last_price:.2f}, 漲幅：{diff:.2f}({diff_ratio:.2%})")
    '''
    
    # Fig2
    if period in ['1d', '5d', '1mo']:
        fig, ax1 = plt.subplots()
        # candle_data = ticker[['Open', 'High', 'Low', 'Close', 'Volume']]
        # fig, ax = mpf.plot(data = candle_data, type = 'candle', style = 'binance', title = search_stock, volume = True, returnfig=True)
        # 直方圖在左邊 Y 軸
        ax1.plot(ticker['Datetime'], ticker['Close'], color='red', marker=None)
        ax1.set_ylabel('股價')
        # 折線圖在右邊 Y 軸
        ax2 = ax1.twinx()
        ax2.bar(ticker['Datetime'], ticker['Volume'], color='lightgreen', width=0.1, alpha=0.5)
        ax2.set_ylabel('成交量')
        ax1.tick_params(axis='x', labelrotation=90)
        fig.suptitle(f"{search_stock}\n現價：{last_price:.2f}, 漲幅：{diff:.2f}({diff_ratio:.2%})")
    else:
        ticker['5SMA'] = ticker['Close'].rolling(window = 5, center = False).mean()
        ticker['30SMA'] = ticker['Close'].rolling(window = 30, center = False).mean()
        candle_data = ticker[['Open', 'High', 'Low', 'Close', 'Volume']]
        LSMA = [ mpf.make_addplot(ticker['5SMA'], color = 'blue'),mpf.make_addplot(ticker['30SMA'], color = 'orange') ]
        fig, ax = mpf.plot(data = candle_data, type = 'candle', style = 'binance', addplot = LSMA, 
                           title = f"{search_stock}\n現價：{last_price:.2f}, 漲幅：{diff:.2f}({diff_ratio:.2%})", volume = True, returnfig=True)
        
    return fig
    
'''
TSMC['5SMA'] = TSMC['Close'].rolling(window = 5, center = False).mean()
TSMC['34SMA'] = TSMC['Close'].rolling(window = 34, center = False).mean()
candle_data = TSMC[['Open', 'High', 'Low', 'Close', 'Volume']]
LSMA = [ mpf.make_addplot(TSMC['5SMA'], color = 'blue'),mpf.make_addplot(TSMC['34SMA'], color = 'orange') ]
mpf.plot(data = candle_data, type = 'candle', style = 'binance', addplot = LSMA, figratio = (18, 10), title = 'TSMC', volume = True)
'''

def calculate_increase_decrease(search_stock, period, ticker):
    # 只有 1d 是看前一天收盤價，其他都是看第一筆收盤價
    if period == '1d':
        yes_ticker = yf.Ticker(search_stock, session=session).history(period='5d')
        # 今天是開盤日，未開盤
        # 今天是開盤日，開盤中
        # 今天是開盤日，已收盤
        yes_price = yes_ticker['Close'].iloc[-2]
        print(yes_ticker)
        # 今天不是開盤日
    else:
        yes_ticker = ticker
        yes_price = yes_ticker['Close'].iloc[0]
    last_price = ticker['Close'].iloc[-1] # 今日收盤/最新收盤
    diff = last_price - yes_price
    diff_ratio = diff / last_price
    
    return diff, diff_ratio, yes_price