# from turtle import pd
import pandas as pd
import config
import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager
import time
from binance import ThreadedWebsocketManager
import matplotlib.pyplot as plt
import websocket
import json
import requests


def on_open(ws):
    print('The socket is open!')
    subscribe_message = {
        'type': 'subscribe',
        'channels': [{
            'name': 'ticker',
            'product_ids': ['BTC-USD']
        }
        ]
    }
    ws.send(json.dumps(subscribe_message))


def on_message(ws, message):
    current_data = json.loads(message)
    print(current_data)


# def handle_socket_message(msg):
#     df = pd.DataFrame([msg])
#     df = df.loc[:, ['s', 'E', 'p']]
#     df.columns = ['symbol', 'Time', 'Price']
#     df.Price = df.Price.astype(float)
#     df.Time = pd.to_datetime(df.Time, unit='ms')
#     df.to_sql('BTCUSDT', engine, if_exists='append', index=False)
#     print(df)


if __name__ == '__main__':
    # symbol = 'BTCUSDT'
    # twm = ThreadedWebsocketManager(config.apiKey, config.apiSecurity)
    # twm.start()
    # twm.start_trade_socket(callback=handle_socket_message, symbol=symbol)
    #  engine = sqlalchemy.create_engine('sqlite:///BTCUSDstream.db')
    #  aux = pd.read_sql('BTCUSDT', engine)
    #  print(aux)
    # plt.plot(aux.Price)
    # plt.show()
    # socket = 'wss://ws-feed.exchange.coinbase.com'
    # ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
    # ws.run_forever()
    # r = requests.get('https://www.coingecko.com/en')
    # df = pd.read_html(r.text)[0]
    # df = df[['Coin', 'Price', 'Mkt Cap']]
    # df['Coin'] = df['Coin'].apply(lambda x: x.split('  ')[0])
    # df['Price'] = df['Price'].apply(lambda x: x.replace(',', '').replace('$', ''))
    # df['Mkt Cap'] = df['Mkt Cap'].apply(lambda x: x.replace(',', '').replace('$', ''))
    # engine = sqlalchemy.create_engine('sqlite:///CoinGecko.db')
    # df.to_sql('Coin', engine, if_exists='append', index=False)
    # # print(df)
    # aux = pd.read_sql('Coin', engine)
    # print(aux)
    print('Hello')

# Mean Reversion simulation
# import pandas as pd
# # import pandas_datareader as pdr
# from binance.client import Client
# from binance import ThreadedWebsocketManager
# from binance import BinanceSocketManager
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import rcParams
# rcParams['figure.figsize'] = 8,6
# import seaborn as sb
# import time
# import config
# import sqlalchemy
# from datetime import datetime
# sb.set()
#
#
# def handle_socket_message(msg):
#     df = pd.DataFrame([msg])
#     df = df.loc[:, ['s', 'E', 'p']]
#     df.columns = ['symbol', 'Time', 'Price']
#     df.Price = df.Price.astype(float)
#     df.Time = pd.to_datetime(df.Time, unit='ms')
#     df.to_sql('BTCUSDT', engine, if_exists='append', index=False)
#     print(df)
#     dateTimeObj = datetime.now()
#     print('System ts:',dateTimeObj)
#
#     # create moving average and add it to our data frame
#     ma = 200
#     btc['ma'] = btc['Price'].rolling(window=ma, min_periods=ma).mean()
#
#     # moving average=determine the direction of a trend, it is continually recalculated based on the latest price data
#     macol = float(btc['ma'][-1:])
#     print('Moving average:',macol)
#     # closing price= the last price at which a stock trades during regular trading session
#     close = float(btc['Price'][-1:])
#     print('Close:',close)
#
#     # define the conditions we will make trades upon
#     # We will want to buy if closing price is greater than the moving average
#     if close > macol:
#         print('Buy')
#     elif close < macol:
#         print('Sell')
#     else:
#         print('Not Trade')
#     print('\n')
#
#     time.sleep(60)
#
# if __name__ == '__main__':
#     symbol = 'BTCUSDT'
#     twm = ThreadedWebsocketManager(config.apiKey, config.apiSecurity)
#     twm.start()
#     twm.start_trade_socket(callback=handle_socket_message, symbol=symbol)
#     engine = sqlalchemy.create_engine('sqlite:///BTCUSDstream.db')
#     btc = pd.read_sql('BTCUSDT', engine)
#     plt.plot(btc.Price)
#     plt.title('BTC Price Chart')
#     plt.show()
#
#     # client data request
#     # client= Client(config.apiKey, config.apiSecurity)
#     # info=client.get_account()
