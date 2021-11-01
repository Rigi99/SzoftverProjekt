import websocket
import json
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import time
import seaborn as sb
from matplotlib import rcParams

engine = sqlalchemy.create_engine('sqlite:///CoinbaseDB.db')
helper = []
rcParams['figure.figsize'] = 8, 6
sb.set()



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
    df = pd.DataFrame([current_data])
    df = df.loc[:, ['product_id', 'time', 'price']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.to_sql('BTCUSDT', engine, if_exists='append', index=False)


def getCoinBaseData():
    socket = 'wss://ws-feed.exchange.coinbase.com'
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
    ws.run_forever()


def movingAverageMethodCoinBase():
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
