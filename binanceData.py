import pandas as pd
import config
import sqlalchemy
from binance import ThreadedWebsocketManager
import matplotlib.pyplot as plt
import time
from matplotlib import rcParams
import seaborn as sb

engine = sqlalchemy.create_engine('sqlite:///BinanceDB.db')
rcParams['figure.figsize'] = 8, 6
sb.set()
helper = []


def handle_socket_message(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['s', 'E', 'p']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    df.to_sql('BTCUSDT', engine, if_exists='append', index=False)


def getBinanceData():
    symbol = 'BTCUSDT'
    twm = ThreadedWebsocketManager(config.apiKey, config.apiSecurity)
    twm.start()
    twm.start_trade_socket(callback=handle_socket_message, symbol=symbol)


def movingAverageMethodBinance():
    btc = pd.read_sql('BTCUSDT', engine)
    movingAverage = float(btc['Price'].mean())
    helper.append(movingAverage)
    print('Moving average=', movingAverage)
    plt.plot(btc.Price, label='Price')
    plt.plot(helper, label='Moving average')
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
