import flask
from flask import request, jsonify
import json
from websocket_API import start_websockt_apis

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Currently supported symbols
ETH = "ETH"
USD = "USD"
# Each symbol data is saved in its mapped file.
symbol_file_map = {ETH:"result1.json", USD:"result2.json"}


@app.route('/api/currency/ETHBTC', methods=['GET'])
def api_ETH():
	"""
		API endpoint for symbol ETHBTC.
	"""
	return jsonify(get_currency_by_symbol(ETH))


@app.route('/api/currency/BTCUSD', methods=['GET'])
def api_USD():
	"""
		API endpoint for symbol BTCUSD
	"""	
	return jsonify(get_currency_by_symbol(USD))


@app.route('/api/currency/all', methods=['GET'])
def api_all():
	"""
		API endpoint for all symbols.
	"""
	data1 = get_currency_by_symbol(USD)
	data2 = get_currency_by_symbol(ETH)
	return jsonify([data1, data2])


def get_currency_by_symbol(symbol):

	file_name = symbol_file_map.get(symbol)
	file = open(file_name)
	data = json.load(file)
	return data

def main():
	"""
		Use localhost:5000/api/currency/{symbol} for the required symbol
		Use localhost:5000/api/currency/ for all the symbols

	"""
	start_websockt_apis()
	app.run()

if __name__ == "__main__":
	main()