# from turtle import pd
import pandas as pd
import config
import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager
import time
from binance import ThreadedWebsocketManager
import matplotlib.pyplot as plt


def handle_socket_message(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['s', 'E', 'p']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    df.to_sql('BTCUSDT', engine, if_exists='append', index=False)
    print(df)


if __name__ == '__main__':
    symbol = 'BTCUSDT'
    twm = ThreadedWebsocketManager(config.apiKey, config.apiSecurity)
    twm.start()
    twm.start_trade_socket(callback=handle_socket_message, symbol=symbol)
    engine = sqlalchemy.create_engine('sqlite:///BTCUSDstream.db')
    aux = pd.read_sql('BTCUSDT', engine)
    print(aux)
    plt.plot(aux.Price)
    plt.show()
