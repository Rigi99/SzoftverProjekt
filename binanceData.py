import logging
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
import binance.enums as be


def handle_socket_message(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['E', 'p']]
    df.columns = ['DAY', 'Price']
    df.Price = df.Price.astype(float)
    df.DAY = pd.to_datetime(df.DAY, unit='ms')
    df.to_sql(config.DbHistorical, config.engineHistorical, if_exists='append', index=False)


def getHistoricalData1Day(Db, eng):
    client = Client(config.apiKey, config.apiSecurity)
    klines = client.get_historical_klines(symbol='BTCBUSD', interval=Client.KLINE_INTERVAL_1DAY,
                                          start_str='15 Oct, 2021')
    df = pd.DataFrame(klines)
    df = df.loc[:, [0, 1]]
    df.columns = ['DAY', 'Price']
    df.DAY = pd.to_datetime(df.DAY, unit='ms')
    df.Price = df.Price.astype(float)
    df.to_sql(Db, eng, if_exists='append', index=False)
    getHistoricalDataAux(Db, eng)


def getHistoricalDataAux(Db, eng):
    client = Client(config.apiKey, config.apiSecurity)
    klines = client.get_historical_klines(symbol='BTCBUSD', interval=Client.KLINE_INTERVAL_1MINUTE,
                                          start_str=datetime.strftime(datetime.today(), '%d %B, %Y'))
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


def getMovingAverages():
    getHistoricalData1Day(config.DbHistorical, config.engineHistorical)
    ma1Day, currentPrice = movingAverageMethodBinance1Day(config.DbHistorical, config.engineHistorical)
    ma7Days, currentPrice = movingAverageMethodBinance7Days(config.DbHistorical, config.engineHistorical)
    ma30Days, currentPrice = movingAverageMethodBinance30Days(config.DbHistorical, config.engineHistorical)
    # ma1Day, currentPrice = 60000, 60000
    # ma7Days, currentPrice = 59000, 60000
    # ma30Days, currentPrice = 58500, 60000
    return ma1Day, ma7Days, ma30Days, currentPrice


def strategy():
    coinBalance, baseBalance = getClientData(symbolCoin='BTC', symbolMoney='BUSD')
    currentBalance = baseBalance
    distanceListSell = [-1]
    distanceListBuy = [-1]
    while True:
        ma1Day, ma7Days, ma30Days, currentPrice = getMovingAverages()
        if currentPrice >= ma30Days and ma7Days >= ma30Days and coinBalance != 0:
            distanceListSell.append(math.sqrt(abs(ma7Days ** 2 - ma30Days ** 2)))
            if distanceListSell[-2] < distanceListSell[-1]:
                if baseBalance < currentPrice * coinBalance:
                    buy(currentBalance=currentBalance, currentPrice=currentPrice)
        elif currentPrice < ma30Days and ma7Days < ma30Days and currentBalance != 0:
            distanceListBuy.append(math.sqrt(abs(ma1Day ** 2 - ma30Days ** 2)))
            if distanceListBuy[-2] < distanceListBuy[-1]:
                sell(currentBalance=currentBalance, currentPrice=currentPrice)
        deleteDataBase(config.DbHistorical + '.db')
        time.sleep(65)
        coinBalance, currentBalance = getClientData(symbolCoin='BTC', symbolMoney='BUSD')


def buy(currentBalance, currentPrice):
    client = Client(config.apiKey, config.apiSecurity)
    buy_quantity = round(currentBalance / currentPrice)
    order = client.create_order(symbol='BTCBUSD', side=be.SIDE_BUY, type=be.ORDER_TYPE_MARKET, quantity=buy_quantity)
    print(order)


def sell(currentBalance, currentPrice):
    client = Client(config.apiKey, config.apiSecurity)
    buy_quantity = round(currentBalance / currentPrice)
    order = client.create_order(symbol='BTCBUSD', side=be.SIDE_SELL, type=be.ORDER_TYPE_MARKET, quantity=buy_quantity)
    print(order)


# f = open('Buy.txt', 'a')
# coinBalance = currentBalance / currentPrice
# currentBalance = 0
# f.write(
#     "Buy" + '\t\t' + str(currentPrice) + '\t\t' + str(datetime.now()) + '\t\t' + str(
#         coinBalance) + '\n')
# f.close()

# f = open('Sell.txt', 'a')
# currentBalance = coinBalance * currentPrice
# coinBalance = 0
# f.write("Sell" + '\t\t' + str(currentPrice) + '\t\t' + str(datetime.now()) + '\t\t' + str(
#     currentBalance) + '\n')
# f.close()
