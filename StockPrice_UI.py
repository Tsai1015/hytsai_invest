import yfinance as yf
import tkinter as tk
import pandas as pd
import sys
import os
import json
import get_TaiwanStock
import draw_Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from curl_cffi import requests
from datetime import date

# 每月重新整理 Taiwan 股票清單
today = date.today()
target_file = f"TaiwanStockList_{today.month:02d}.txt"

if os.path.exists(target_file):
    with open(target_file, "r") as f:
        content = f.read()
    Taiwan_stock = content.strip().split(",")
else:
    Taiwan_stock = get_TaiwanStock.create_TaiwanStock(today.month)
    with open(target_file, 'w') as f:
        f.write(",".join(Taiwan_stock))

# overall UI
root = tk.Tk()
root.title('歷史股價')
root.geometry('800x800')

# variable definition
stock_id = tk.StringVar()
period_selected = tk.StringVar(value="1d")
canvas = None

# function definition
def show():
    search_stock = stock_id.get()
    period = period_selected.get()
    if search_stock in Taiwan_stock:
        stock_mode = 1 # 台股
        search_stock = search_stock + ".TW"
    else:
        stock_mode = 2 # 美股
    session = requests.Session(impersonate="chrome")
    if period == '1d':
        ticker = yf.Ticker(search_stock, session=session).history(period=period, interval='5m')
    elif period == '5d':
        ticker = yf.Ticker(search_stock, session=session).history(period=period, interval='30m')
    else:
        ticker = yf.Ticker(search_stock, session=session).history(period=period) # period_selected.get()
    
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
        
    fig = draw_Figure.draw_fig(search_stock, period, ticker)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    print(ticker)
    
def on_closing():
    root.quit()   # 安全地退出 mainloop()
    sys.exit()    # 完全結束 Python 程式

# 輸入區
enter_block = tk.Frame(root)
enter_block.pack(anchor="nw", pady=10, padx=10)
ask_label = tk.Label(enter_block, text="請輸入股票代號：")
ask_label.pack(side="left", padx=(10, 0), pady=20)
ask_entry = tk.Entry(enter_block, textvariable=stock_id)
ask_entry.pack(side="left", padx=(5, 10))
search = tk.Button(enter_block, text='查詢', command=show)
search.pack(side="left")

# 區間選擇區
period_frame = tk.Frame(root)
period_frame.pack(anchor="nw", pady=5, padx=10)

period_label_map = {
    "1d": "一日",
    "5d": "五日",
    "1mo": "一個月",
    "6mo": "六個月",
    "1y": "一年",
    "5y": "五年",
    "max": "最久"
}

for value, label_text in period_label_map.items():
    rb = tk.Radiobutton(period_frame, text=label_text, variable=period_selected, value=value, command=show)
    rb.pack(side="left", padx=5)
    
# 繪圖區

# icon 區
icon = tk.PhotoImage(file="Nana.png")
root.iconphoto(True, icon)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

# 找不到股票代號
# 回測
# 漲幅修正前日收盤