import requests
import json
import websocket
from websocket import create_connection
from threading import Lock, Thread
import flask
from flask import request, jsonify

# API end-points
symbol_url = "https://api.hitbtc.com/api/2/public/symbol/"
ticker_url = "https://api.hitbtc.com/api/2/public/ticker/"
currency_url = "https://api.hitbtc.com/api/2/public/currency/"
url = "wss://api.hitbtc.com/api/2/ws"


class Symbol:
	"""
		Data Model to represent the response.

	"""
	def __init__(self, fullName=None, id=None, ask=None, bid=None, last=None, open=None, low=None, high=None, feeCurrency=None):
		self.fullName = fullName
		self.id = id
		self.ask = ask
		self.bid = bid
		self.last = last
		self.open = open
		self.low = low
		self.high = high
		self.feeCurrency = feeCurrency

	def set_symbol_data(self, feeCurr):
		self.feeCurrency = feeCurr
	
	def set_currency_data(self, id, fullName):
		self.id = id;
		self.fullName = fullName

	def set_ticker_data(self, ask, bid, last, low, high, open):
		self.ask = ask
		self.bid = bid
		self.last = last
		self.low = low
		self.high = high
		self.open = open

	def __repr__(self):
		return {"id":self.id, "fullName":self.fullName, "ask":self.ask, "bid":self.bid, "last":self.last, "open":self.open, "low":self.low, "high":self.high, "feeCurrency":self.feeCurrency}


lock = Lock()
message_list = [] 

def collect_server1_data():
	"""
		- Get Ticker data for the first symbol.
		- Using socket connection to get the Information from Ticker api
		- Using HTTP connection to get the information from Currency and  Symbol api
		- Saving the Symbol data representing the required information from symbol, currecny and ticker api, in json form.

	"""
	global message_list
	bln_running = True
	ws_a = create_connection("wss://api.hitbtc.com/api/2/ws")
	data = {
	"method": "subscribeTicker",
	"params": {
	"symbol": "ETHBTC"
	},
	"id": 123
	}
	ws_a.send(json.dumps(data))
	obj = Symbol()
	r = requests.get(symbol_url+"ETHBTC")
	data = r.json()
	obj.set_symbol_data(data["feeCurrency"])
	# print(data)
	r2 = requests.get(currency_url+data["baseCurrency"])
	data2 = r2.json()
	obj.set_currency_data(data2["id"], data2["fullName"])
	while bln_running:   
		response_a =  json.loads(ws_a.recv())
		if "params" in response_a:
			data_a = response_a["params"]
			obj.set_ticker_data(data_a["ask"], data_a["bid"], data_a["last"], data_a["low"], data_a["high"], data_a["open"])
		lock.acquire()
		message_list.append(response_a)
		lock.release()
		with open('result1.json', 'w') as fp:
			json.dump(obj.__repr__(), fp)
	

def collect_server2_data(): 

	"""
		- Get Ticker data for the second symbol.
		- Using socket connection to get the Information from Ticker api
		- Using HTTP connection to get the information from Currency and  Symbol api
		- Saving the Symbol data representing the required information from symbol, currecny and ticker api, in json form.
		 
	"""
	global message_list
	bln_running = True
	ws_b = create_connection("wss://api.hitbtc.com/api/2/ws")
	data = {
	"method": "subscribeTicker",
	"params": {
	"symbol": "BTCUSD"
	},
	"id": 123
	}
	ws_b.send(json.dumps(data))
	obj = Symbol()
	r = requests.get(symbol_url+"BTCUSD")
	data = r.json()
	obj.set_symbol_data(data["feeCurrency"])
	# print(data)
	r2 = requests.get(currency_url+data["baseCurrency"])
	data2 = r2.json()
	obj.set_currency_data(data2["id"], data2["fullName"])
	while bln_running:
		response_b =  json.loads(ws_b.recv())
		if "params" in response_b:
			data_b = response_b["params"]
			# print(data_b)
			obj.set_ticker_data(data_b["ask"], data_b["bid"], data_b["last"], data_b["low"], data_b["high"], data_b["open"])
		lock.acquire()
		message_list.append(response_b)
		lock.release()
		# print(obj.__repr__())
		res = obj.__repr__()
		with open('result2.json', 'w') as fp:
			json.dump(obj.__repr__(), fp)
	

def start_websockt_apis():
	"""
		Using Threading to run two different methods in parallel.

	"""
	threads = []
	for func in [collect_server1_data, collect_server2_data]:
		threads.append(Thread(target=func))
		threads[-1].start()