from websocket import create_connection
import redis
import json
import time
import threading
import requests
import flask
from flask import request, jsonify


app = flask.Flask(__name__)
app.config["DEBUG"] = True
symbols = ["ETHBTC", "BTCUSDT"]


@app.route('/app/currency/<symbol>', methods=['GET'])
def get_symbol_info(symbol):
    redis_conn = redis.Redis(connection_pool=pool)
    if symbol == "all":
        final_response = []
        for symbol in symbols:
            dynamic_data = json.loads(redis_conn.get(f'ticker/1s_{symbol}'))
            static_data = json.loads(redis_conn.get(f'symbol_{symbol}'))
            response = {key: value for (key, value) in
                        list(dynamic_data.items()) + list(static_data.items())}
            final_response.append(response)
        return jsonify(final_response)
    else:
        dynamic_data = json.loads(redis_conn.get(f'ticker/1s_{symbol}'))
        static_data = json.loads(redis_conn.get(f'symbol_{symbol}'))
        response = {key: value for (key, value) in
                    list(dynamic_data.items()) + list(static_data.items())}
        return jsonify(response)


def get_data(conn, redis_conn):
    while(True):
        time.sleep(1)
        data = json.loads(conn.recv())

        if "result" in data:
            print(f'Subscribed to {data["result"]["ch"]} : {data}\n')
        else:
            for k, v in data["data"].items():
                result = {
                    "ask": v["a"],
                    "bid": v["b"],
                    "last": v["c"],
                    "open": v["o"],
                    "low": v["l"],
                    "high": v["h"],

                }
                redis_conn.set('{}_{}'.format(
                    data["ch"], k), json.dumps(result))
                # print(f'\n\nFrom redis {redis_conn.get(k)}\n\n')

            print(f'Received data for {data["ch"]} : {data}\n')


def subscribe_symbols(redis_conn, symbols):
    for symbol in symbols:
        symbol_response = requests.get(
            "https://api.hitbtc.com/api/3/public/symbol/" + symbol)
        symbol_data = json.loads(symbol_response.text)
        currency_response = requests.get(
            "https://api.hitbtc.com/api/3/public/currency/" + symbol_data["base_currency"])
        currency_data = json.loads(currency_response.text)
        print(currency_data)

        data = {
            "id": symbol_data["base_currency"],
            "fullName": currency_data["full_name"],
            "feeCurrency": "BTC"
        }
        redis_conn.set(f'symbol_{symbol}', json.dumps(data))


def subscribe_ticker(conn, symbols):

    data = {
        "method": "subscribe",
        "ch": "ticker/1s",
        "params": {
            "symbols": symbols
        },
        "id": 123
    }
    conn.send(json.dumps(data))
    print(f'Sending subsription request for ticker data\n')


def subscribe_mini_ticker(conn, symbols):

    data = {
        "method": "subscribe",
        "ch": "ticker/price/1s",
        "params": {
            "symbols": symbols
        },
        "id": 123
    }
    conn.send(json.dumps(data))
    print(f'Sending subsription request for mini-ticker data\n')


def subscribe_candles(conn, symbols):

    data = {
        "method": "subscribe",
        "ch": "ticker/1s",
        "params": {
            "symbols": symbols
        },
        "id": 123
    }
    conn.send(json.dumps(data))
    print(f'Sending subsription request for candles data\n')


def subscribe_orderbook(conn, symbols):

    data = {
        "method": "subscribe",
        "ch": "orderbook/top/100ms/batch",
        "params": {
            "symbols": symbols
        },
        "id": 123
    }
    conn.send(json.dumps(data))
    print(f'Sending subsription request for orderbook data\n')


def connect():
    uri = "wss://api.hitbtc.com/api/3/ws/public"
    conn = create_connection(uri)
    print(f'Client connected\n')
    return conn


if __name__ == '__main__':
    conn = connect()
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    redis_conn = redis.Redis(connection_pool=pool)

    subscribe_symbols(redis_conn, symbols)
    subscribe_ticker(conn, symbols)
    subscribe_candles(conn, symbols)
    subscribe_mini_ticker(conn, symbols)
    subscribe_orderbook(conn, symbols)

    thread = threading.Thread(target=get_data, args=(conn, redis_conn,))

    thread.start()
    app.run()
    thread.join()

# get_data(conn, redis_conn)
