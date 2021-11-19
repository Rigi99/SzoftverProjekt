import math
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
# twm = ThreadedWebsocketManager(config.apiKey, config.apiSecurity)
# twm.start()
# twm.stop()
# symbol = 'BTCBUSD'
# twm.start_trade_socket(callback=handle_socket_message, symbol=symbol)


def handle_socket_message(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['E', 'p']]
    df.columns = ['DAY', 'Price']
    df.Price = df.Price.astype(float)
    df.DAY = pd.to_datetime(df.DAY, unit='ms')
    df.to_sql(config.DbHistorical, config.engineHistorical, if_exists='append', index=False)


def getHistoricalData1Day(Db, eng):
    client = Client(config.apiKey, config.apiSecurity)
    klines = client.get_historical_klines(symbol='BTCBUSD', interval=Client.KLINE_INTERVAL_1DAY, start_str='15 Oct, 2021')
    df = pd.DataFrame(klines)
    df = df.loc[:, [0, 1]]
    df.columns = ['DAY', 'Price']
    df.DAY = pd.to_datetime(df.DAY, unit='ms')
    df.Price = df.Price.astype(float)
    df.to_sql(Db, eng, if_exists='append', index=False)
    getHistoricalDataAux(Db, eng)


def getHistoricalDataAux(Db, eng):
    client = Client(config.apiKey, config.apiSecurity)
    klines = client.get_historical_klines(symbol='BTCBUSD', interval=Client.KLINE_INTERVAL_1MINUTE, start_str=datetime.strftime(datetime.today(), '%d %B, %Y'))
    df = pd.DataFrame(klines)
    df = df.loc[:, [0, 1]]
    df.columns = ['DAY', 'Price']
    df.DAY = pd.to_datetime(df.DAY, unit='ms')
    df.Price = df.Price.astype(float)
    df.iloc[-1:].to_sql(Db, eng, if_exists='append', index=False)


def deleteDataBase(Db):
    import os
    if os.path.exists(Db):
        os.remove(Db)
    else:
        print("The file does not exist")


def getClientData(symbolCoin, symbolMoney):
    # clientAsset = Client(config.apiKey, config.apiSecurity)
    # data = clientAsset.get_account()
    # for it in data['balances']:
    #     print(it)
    coinAmount = 0
    baseBalance = 0
    with open('data.json', 'r') as file:
        data = json.load(file)
    for it in data['balances']:
        # print(it['asset'], it['free'])
        if it['asset'] == symbolCoin:
            coinAmount = float(it['free'])
        if it['asset'] == symbolMoney:
            baseBalance = float(it['free'])
    return coinAmount, baseBalance
    # print(clientAsset.get_asset_balance('USDT'))


def movingAverageMethodBinance1Day(Db, eng):
    btc = pd.read_sql(Db, eng)
    movingAverage = btc.Price.iloc[-1]
    return movingAverage, btc.Price.iloc[-1]


def movingAverageMethodBinance7Days(Db, eng):
    btc = pd.read_sql(Db, eng)
    ma = 7
    btc['ma'] = btc['Price'].rolling(window=ma, min_periods=ma).mean()
    movingAverage = float(btc['ma'][-1:])
    return movingAverage, btc.Price.iloc[-1]


def movingAverageMethodBinance30Days(Db, eng):
    btc = pd.read_sql(Db, eng)
    ma = 30
    btc['ma'] = btc['Price'].rolling(window=ma, min_periods=ma).mean()
    movingAverage = float(btc['ma'][-1:])
    return movingAverage, btc.Price.iloc[-1]


def run():
    coinBalance, baseBalance = getClientData(symbolCoin='BTC', symbolMoney='BUSD')
    currentBalance = baseBalance
    getHistoricalData1Day(config.DbHistorical, config.engineHistorical)
    # aux = pd.read_sql(config.DbHistorical, config.engineHistorical)
    # print(aux)
    while True:
        # ma1Day, currentPrice = movingAverageMethodBinance1Day(config.DbHistorical, config.engineHistorical)
        # ma7Days, currentPrice = movingAverageMethodBinance7Days(config.DbHistorical, config.engineHistorical)
        # ma30Days, currentPrice = movingAverageMethodBinance30Days(config.DbHistorical, config.engineHistorical)
        # print(str(ma1Day) + '\t\t' + str(currentPrice))
        # print(str(ma7Days) + '\t\t' + str(currentPrice))
        # print(str(ma30Days) + '\t\t' + str(currentPrice))
        ma1Day, currentPrice = 60000, 60000
        ma7Days, currentPrice = 59000, 60000
        ma30Days, currentPrice = 58500, 60000
        distanceListSell = [-1]
        distanceListBuy = [-1]
        if currentPrice >= ma30Days and ma7Days >= ma30Days and coinBalance != 0:
            distanceListSell.append(math.sqrt(abs(ma7Days ** 2 - ma30Days ** 2)))
            if distanceListSell[-2] < distanceListSell[-1]:
                if baseBalance < currentPrice * coinBalance:
                    f = open('Sell.txt', 'a')
                    currentBalance = coinBalance * currentPrice
                    coinBalance = 0
                    f.write("Sell" + '\t\t' + str(currentPrice) + '\t\t' + str(datetime.now()) + '\t\t' + str(currentBalance) + '\n')
                    f.close()
        elif currentPrice < ma30Days and ma7Days < ma30Days and currentBalance != 0:
            distanceListBuy.append(math.sqrt(abs(ma1Day ** 2 - ma30Days ** 2)))
            if distanceListBuy[-2] < distanceListBuy[-1]:
                f = open('Buy.txt', 'a')
                coinBalance = currentBalance / currentPrice
                currentBalance = 0
                f.write("Buy" + '\t\t' + str(currentPrice) + '\t\t' + str(datetime.now()) + '\t\t' + str(coinBalance) + '\n')
                f.close()
        deleteDataBase(config.DbHistorical + '.db')
        time.sleep(65)
        getHistoricalData1Day(config.DbHistorical, config.engineHistorical)
        # coinBalance, baseBalance = getClientData(symbolCoin='BTC', symbolMoney='BUSD')
        # aux = pd.read_sql(config.DbHistorical, config.engineHistorical)
        # print(aux)
    deleteDataBase(config.DbHistorical + '.db')
