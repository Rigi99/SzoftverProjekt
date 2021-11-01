import websocket
import json
import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///CoinbaseDB.db')


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
