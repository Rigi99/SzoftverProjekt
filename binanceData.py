import pandas as pd
import config
import sqlalchemy
from binance import ThreadedWebsocketManager
import matplotlib.pyplot as plt
import time
from matplotlib import rcParams
import seaborn as sb
from binance.client import Client


engine = sqlalchemy.create_engine('sqlite:///BinanceDB.db')
rcParams['figure.figsize'] = 8, 6
sb.set()
helper = []


def handle_socket_message(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['s', 'E', 'p']]
    print(df)
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    df.to_sql('BTCUSDT', engine, if_exists='append', index=False)


def getBinanceData():
    symbol = 'BTCUSDT'
    twm = ThreadedWebsocketManager(config.apiKey, config.apiSecurity)
    twm.start()
    twm.start_trade_socket(callback=handle_socket_message, symbol=symbol)


def movingAverageMethodBinance(Db):
    btc = pd.read_sql(Db, engine)
    # movingAverage = float(btc['Price'].mean())
    # helper.append(movingAverage)
    # movingAverage = float(btc['Price'].mean())
    # helper.append(movingAverage)
    ma = 200
    btc['ma'] = btc['Closing'].rolling(window=ma, min_periods=ma).mean()
    movingAverage = float(btc['ma'][-1:])
    print('Moving average=', movingAverage)
    plt.plot(btc.Closing, label='Price')
    plt.plot(btc.ma, label='Moving average')
    plt.title('BTC Price Chart')
    plt.legend()
    plt.show()
    if btc.iloc[-1] > movingAverage:
        print('Buy')
    elif btc.iloc[-1] < movingAverage:
        print('Sell')
    else:
        print('Not Trade')
    print('\n')

    time.sleep(1)


def getHistoricalData(Db):
    deleteDataBase()
    client = Client(config.apiKey, config.apiSecurity)
    klines = client.get_historical_klines(symbol='BTCUSDT', interval='1d', start_str='16 Apr, 2021')
    df = pd.DataFrame(klines)
    df = df.loc[:, [0, 1, 2, 3, 4, 5]]
    df.columns = ['DAY', 'Price', 'Highest', 'Lowest', 'Closing', 'Volume']
    df.DAY = pd.to_datetime(df.DAY, unit='ms')
    df.Price = df.Price.astype(float)
    df.Highest = df.Highest.astype(float)
    df.Lowest = df.Lowest.astype(float)
    df.Closing = df.Closing.astype(float)
    df.Volume = df.Volume.astype(float)
    df.to_sql(Db, engine, if_exists='append', index=False)
    aux = pd.read_sql(Db, engine)
    print(aux)

def deleteDataBase():
    import os
    if os.path.exists("BinanceDB.db"):
        os.remove("BinanceDB.db")
    else:
        print("The file does not exist")