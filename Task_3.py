#In ByBit API you can't get more than 200 bars from it. 
#So if you need to get data for a large portion of the time you have to call it multiple times.
#Here is the code you can use to get data for the entire history of 1-minute bars for BTCUSD:



import requests 
import json 
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import time
import pytz
import talib as ta
from concurrent.futures import ThreadPoolExecutor





def get_bybit_bars(symbol, interval, startTime, endTime):
    try:
 
        url = "https://api.bybit.com/v2/public/kline/list"
        startTime = str(int(startTime.timestamp()))
        endTime   = str(int(endTime.timestamp()))
        params = {
            "symbol" : symbol,
            'interval' : interval,
            'from' : startTime,
            'to' : endTime
        }

        response=requests.get(url, params = params)
        response=json.loads(response.text)
        dataDict=response['result']
        df = pd.DataFrame(dataDict)
    
        if (len(df.index) == 0):
            return None 
        


        sit_tz = pytz.timezone('Asia/Kolkata')
        df.index = [dt.datetime.fromtimestamp(x, tz=sit_tz) for x in df.open_time]
        df['SMA'] = ta.SMA(df['close'], timeperiod=10)
        
        df['volume'] = pd.to_numeric(df['volume'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['close'] = pd.to_numeric(df['close'])
        df['VWAP'] = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()

        macd, macd_signal, macd_hist = ta.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        df['MACD'] = macd
        df['MACD_signal'] = macd_signal
        df['MACD_hist'] = macd_hist
        return df
    except:
        print(f'some thing wrong with{symbol} ')
        return None


def data(symbol):
    df_list = []
    last_datetime = dt.datetime(2021, 1, 1)
    til_date=dt.datetime(2022, 12, 31) #dt.datetime.now()

    while True:
        print(last_datetime)
        new_df = get_bybit_bars(symbol, 15, last_datetime, til_date)
        if new_df is None:
            break
        df_list.append(new_df)
        last_datetime = max(new_df.index) + dt.timedelta(0, 1)
        time.sleep(2)
    
    if len(df_list)==0:
        print(f'something wrong with{symbol}')
        return pd.DataFrame()
    df = pd.concat(df_list)
    df.to_csv(f'{symbol}.csv')
    return df


import threading
threads = []
SYMBOLS = ['BTCUSD', 'ETHUSD', 'BITUSD','SOLUSD', 'XRPUSD']

for symbol in SYMBOLS:
    t = threading.Thread(target=data, args=(symbol,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("All data saved to CSV")