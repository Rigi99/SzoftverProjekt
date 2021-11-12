import pandas as pd
import config
from binance import ThreadedWebsocketManager
import matplotlib.pyplot as plt
import time
from matplotlib import rcParams
import seaborn as sb
from binance.client import Client
import json
import numpy as np
from datetime import datetime

rcParams['figure.figsize'] = 8, 6
sb.set()
helper = []


def handle_socket_message(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['s', 'E', 'p']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    df.to_sql(config.DbRealTime, config.engineRealTime, if_exists='append', index=False)
    aux = pd.read_sql(config.DbRealTime, config.engineRealTime)
    print(aux)


def getBinanceData():
    symbol = 'BTCBUSD'
    twm = ThreadedWebsocketManager(config.apiKey, config.apiSecurity)
    twm.start()
    twm.start_trade_socket(callback=handle_socket_message, symbol=symbol)
    twm.stop()


def movingAverageMethodBinance(Db):
    btc = pd.read_sql(Db, config.engineHistorical)
    ma = 200
    btc['ma'] = btc['Closing'].rolling(window=ma, min_periods=ma).mean()
    movingAverage = float(btc['ma'][-1:])
    # plt.plot(btc.Closing, label='Closing')
    # plt.plot(btc.ma, label='Moving average')
    # plt.plot(movingAverage, label='Moving average')
    # plt.title('BTC Price Chart')
    # plt.legend()
    # plt.show()
    f = open("output.txt", "a")
    if btc.Price.iloc[-1] <= movingAverage:
        f.write("BUY!\t")
        f.write(str(btc.Price.iloc[-1]))
        f.write('\t')
        f.write(str(movingAverage))
        f.write('\t\t')
        f.write(str(datetime.now()))
        f.write('\n**************************************************\n')
        f.close()
    else:
        f.write("SELL!\t")
        f.write(str(btc.Price.iloc[-1]))
        f.write('\t')
        f.write(str(movingAverage))
        f.write('\t\t')
        f.write(str(datetime.now()))
        f.write('\n**************************************************\n')
        f.close()
    deleteDataBase(Db + '.db')
    print('DONE!')


def getHistoricalData(Db):
    client = Client(config.apiKey, config.apiSecurity)
    klines = client.get_historical_klines(symbol='BTCBUSD', interval='30m', start_str='16 Apr, 2021')
    df = pd.DataFrame(klines)
    df = df.loc[:, [0, 1, 2, 3, 4, 5]]
    df.columns = ['DAY', 'Price', 'Highest', 'Lowest', 'Closing', 'Volume']
    df.DAY = pd.to_datetime(df.DAY, unit='ms')
    df.Price = df.Price.astype(float)
    df.Highest = df.Highest.astype(float)
    df.Lowest = df.Lowest.astype(float)
    df.Closing = df.Closing.astype(float)
    df.Volume = df.Volume.astype(float)
    df.to_sql(Db, config.engineHistorical, if_exists='append', index=False)
    aux = pd.read_sql(Db, config.engineHistorical)
    # print(aux)


def deleteDataBase(Db):
    import os
    if os.path.exists(Db):
        os.remove(Db)
    else:
        print("The file does not exist")


def getClientData():
    # clientAsset = Client(config.apiKey, config.apiSecurity)
    # data = clientAsset.get_account()
    # for it in data['balances']:
    #     print(it)
    with open('data.json', 'r') as file:
        data = json.load(file)
    for it in data['balances']:
        print(it)
    # print(clientAsset.get_asset_balance('USDT'))
