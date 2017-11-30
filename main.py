from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
from account import get_balance
from ma_generator import MAGenerator
from secrets import API_KEY
from secrets import API_SECRET

SYMBOL = "EOSETH"
INTERVAL = KLINE_INTERVAL_15MINUTE
BALANCE = 0.03716156
ma_durations = [7, 25, 99]
client = Client(API_KEY, API_SECRET)
print get_balance(client, "ETH")

ma_generator = MAGenerator(client,SYMBOL,ma_durations,INTERVAL)
print ma_generator.get_mas()

# # place market buy order
# from binance.enums import *

def create_order(price):
	qty = 0
	order = client.get_account()
	for balance in order['balances']:
		if balance["asset"]=="ETH":
			qty = float(balance["free"])
	if qty == 0:
		return
	order_qty = "{:0.2f}".format(str(qty/price))
	print(order_qty)
	# order = client.create_order(
	# 	symbol=SYMBOL,
	# 	side=SIDE_BUY,
	# 	type=ORDER_TYPE_LIMIT,
	# 	price=str(price),
	# 	quantity=100)


# start trade websocket
def process_message(msg):
	if msg['e']=="kline":
		print(msg)
	elif msg['e']=="trade":
		print(msg['s'])
		print(msg)

# do something
bm = BinanceSocketManager(client)
# print(bm.start_kline_socket(SYMBOL, process_message, interval=INTERVAL))
print(bm.start_trade_socket(SYMBOL, process_message))
bm.start()