import math
import pandas as pd
import config
import time
from binance.client import Client
from datetime import datetime
import binance.enums as be


def handle_socket_message(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['E', 'p']]
    df.columns = ['DAY', 'Price']
    df.Price = df.Price.astype(float)
    df.DAY = pd.to_datetime(df.DAY, unit='ms')
    df.to_sql(config.DbHistorical, config.engineHistorical, if_exists='append', index=False)
    # This function formats the response message from the API, we only need the price and the timestamp, so we get only
    # those columns. After we have the data we need, we store it in a database.


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
    # In this function we get the historical data about a specified coin. We have to specify a starting date, and an
    # interval, now it is set to 1 day, this means that we get 1 record for the past days. We also store these in a
    # database.


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
    # This function appends the current price for a specified coin to the historical database, we do this for the
    # accuracy of the moving averages.


def deleteDataBase(Db):
    import os
    if os.path.exists(Db):
        os.remove(Db)
    else:
        print("The file does not exist")
    # This is a simple database deleting function.


def getClientData(symbolCoin, symbolMoney):
    clientAsset = Client(config.apiKey, config.apiSecurity)
    data = clientAsset.get_account()
    coinAmount = 0
    baseBalance = 0
    for it in data['balances']:
        if it['asset'] == symbolCoin:
            coinAmount = float(it['free'])
        if it['asset'] == symbolMoney:
            baseBalance = float(it['free'])
    return coinAmount, baseBalance
    # This function returns the clients coin balance and the clients money balance.


def movingAverageMethodBinance1Day(Db, eng):
    btc = pd.read_sql(Db, eng)
    movingAverage = btc.Price.iloc[-1]
    return movingAverage, btc.Price.iloc[-1]
    # In this function we calculate the 1 day moving average.


def movingAverageMethodBinance7Days(Db, eng):
    btc = pd.read_sql(Db, eng)
    ma = 7
    btc['ma'] = btc['Price'].rolling(window=ma, min_periods=ma).mean()
    movingAverage = float(btc['ma'][-1:])
    return movingAverage, btc.Price.iloc[-1]
    # In this function we calculate the 6 day moving average.


def movingAverageMethodBinance30Days(Db, eng):
    btc = pd.read_sql(Db, eng)
    ma = 30
    btc['ma'] = btc['Price'].rolling(window=ma, min_periods=ma).mean()
    movingAverage = float(btc['ma'][-1:])
    return movingAverage, btc.Price.iloc[-1]
    # In this function we calculate the 30day moving average.


def getMovingAverages():
    getHistoricalData1Day(config.DbHistorical, config.engineHistorical)
    ma1Day, currentPrice = movingAverageMethodBinance1Day(config.DbHistorical, config.engineHistorical)
    ma7Days, currentPrice = movingAverageMethodBinance7Days(config.DbHistorical, config.engineHistorical)
    ma30Days, currentPrice = movingAverageMethodBinance30Days(config.DbHistorical, config.engineHistorical)
    # ma1Day, currentPrice = 60000, 60000
    # ma7Days, currentPrice = 59000, 60000
    # ma30Days, currentPrice = 58500, 60000
    return ma1Day, ma7Days, ma30Days, currentPrice
    # In this function we return the different moving averages, and the current price.


def strategy():
    coinBalance, baseBalance = getClientData(symbolCoin='BTC', symbolMoney='BUSD')
    ma1Day, ma7Days, ma30Days, currentPrice = getMovingAverages()
    currentBalance = baseBalance
    distanceListSell = [math.sqrt(abs(ma7Days ** 2 - ma30Days ** 2))]
    distanceListBuy = [math.sqrt(abs(ma1Day ** 2 - ma30Days ** 2))]
    while True:
        ma1Day, ma7Days, ma30Days, currentPrice = getMovingAverages()
        if currentPrice >= ma30Days and ma7Days >= ma30Days and coinBalance != 0:
            distanceListSell.append(math.sqrt(abs(ma7Days ** 2 - ma30Days ** 2)))
            if distanceListSell[-2] > distanceListSell[-1]:
                if baseBalance < currentPrice * coinBalance:
                    sell(coinBalance=coinBalance)
        elif currentPrice < ma30Days and ma7Days < ma30Days and currentBalance != 0:
            distanceListBuy.append(math.sqrt(abs(ma1Day ** 2 - ma30Days ** 2)))
            if distanceListBuy[-2] > distanceListBuy[-1]:
                buy(currentBalance=currentBalance, currentPrice=currentPrice)
        deleteDataBase(config.DbHistorical + '.db')
        time.sleep(65)
        coinBalance, currentBalance = getClientData(symbolCoin='BTC', symbolMoney='BUSD')
    # This is the main function. Here is implemented the strategy. First, we get the clients balances, and the moving
    # averages. Then the 2 lists we use are used to follow the different moving average changes. We calculate the
    # distance between the moving averages, because we use these distances to decide to buy or sell coins. In an
    # infinite loop we start the considering process. We get the moving averages, and then in the if statements we
    # check some aspects to make a good decision in buying or selling coins. We check the current price and the 7 day
    # moving average, because when the current price and the 7 day average is above the 30 day average, it is a good
    # moment to sell our coins. This last smaller statement, where we check our base balance and the balance we will
    # have after selling, guarantees profit. When we create a buying order, we make sure that the current price and
    # the 7 day average is under the 30 day average, because tha is the moment when the coin has a very low price for
    # a longer period. The buying order is placed when the distance between the 1 day average and the 30 day average
    # drops, because this shows that the price began to increase. The selling order is placed when the distance between
    # the 7 day average and the 30 day average drops. We use here the 7 day average, because if the current price drops
    # for example now, it would immediately sell, but it could re-rise in 1 hour, and this doesn't effects that much the
    # 7 day average, so it's better to work here with that. After placing an order, we delete tha database, because we
    # have to be up to date, and at the beginning of the loop we rebuild always it.


def buy(currentBalance, currentPrice):
    client = Client(config.apiKey, config.apiSecurity)
    buy_quantity = round(currentBalance / currentPrice)
    order = client.create_order(symbol='BTCBUSD', side=be.SIDE_BUY, type=be.ORDER_TYPE_MARKET, quantity=buy_quantity)
    print(order)
    # This function creates and places a coin buying order.


def sell(coinBalance):
    client = Client(config.apiKey, config.apiSecurity)
    sell_quantity = coinBalance
    order = client.create_order(symbol='BTCBUSD', side=be.SIDE_SELL, type=be.ORDER_TYPE_MARKET, quantity=sell_quantity)
    print(order)
    # This function creates and places a coin selling order.

