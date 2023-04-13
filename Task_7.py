import json
import websocket
import time

#FORMAT OF STREAMING MESSAGE
'''{
'topic': 'orderbook.1.BTCUSDT', 
 'ts': 1681389126625, 
 'type': 'snapshot', 
 'data': {
    's': 'BTCUSDT', 
    'b': [['30203.53', '1.892437']], 
    'a': [['30203.54', '0.000301']], 
    'u': 23137959, 
    'seq': 4498102785
  }
}'''

api_key = ""
api_secret = ""


def on_open(ws):
    print('---------OPEN----------')
    print("Connection opened")

    subscribe_data = {
        "req_id": "test", 
        "op": "subscribe",
        "args": [
            "orderbook.1.BTCUSDT"
    ]
    }
    #Telling bybit Api start streaming sunscribed data
    ws.send(json.dumps(subscribe_data))

def on_error(ws, error):
    print('---------ERROR----------')
    # print(error)

def on_close(ws):
    print('---------CLOSE---------')
    



def on_message(ws, message):
    print('---------MESSAGE----------')
    data = json.loads(message)
    print(data)
    if 'topic' in data:
        if data['topic'] == 'orderbook.1.BTCUSDT':
            print(data['topic'])
            bids = data['data']['b'][0]
            asks = data['data']['a'][0]
            print("Bids:")
            for bid in bids:
                print(f"Price: {bid[0]}  Quantity: {bid[1]}")
            print("Asks:")
            for ask in asks:
                print(f"Price: {ask[0]}  Quantity: {ask[1]}")
    time.sleep(10)






websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://stream.bybit.com/v5/public/spot",
                            on_open=on_open,
                            on_error=on_error,
                            on_close=on_close,
                            on_message=on_message,
                           )

ws.run_forever()












