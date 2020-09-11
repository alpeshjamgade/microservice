# microservice
Create a micro-service with the following endpoint:

* GET /current/{symbol}

* GET /current/all

# How to use
run script api.py

# Dependencies
pip install -r requirements.txt

# Example
GET/current/{symbol}
* http://127.0.0.1:5000/api/currency/ETHBTC
* http://127.0.0.1:5000/api/currency/BTCUSD

`
{
"id": "ETH",
"fullName": "Ethereum",
"ask": "0.054464",
"bid": "0.054463",
"last": "0.054463",
"open": "0.057133",
"low": "0.053615",
"high": "0.057559",
"feeCurrency": "BTC"
}
`

GET /currency/all
* http://127.0.0.1:5000/api/currency/all

`
[
  {
    "ask": "10281.92", 
    "bid": "10281.54", 
    "feeCurrency": "USD", 
    "fullName": "Bitcoin", 
    "high": "10484.94", 
    "id": "BTC", 
    "last": "10282.10", 
    "low": "10196.14", 
    "open": "10386.03"
  }, 
  {
    "ask": "0.035456", 
    "bid": "0.035453", 
    "feeCurrency": "BTC", 
    "fullName": "Ethereum", 
    "high": "0.036060", 
    "id": "ETH", 
    "last": "0.035451", 
    "low": "0.034860", 
    "open": "0.035930"
  }
]
`
