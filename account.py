def get_balance(client, symbol="ETH"):
	order = client.get_account(recvWindow=5000)
	qty = -1
	for balance in order['balances']:
		if balance["asset"] == symbol:
			qty = balance["free"]
	return qty