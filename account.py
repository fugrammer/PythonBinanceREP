def get_balance(client, symbol="ETH"):
	# order = client.get_account(recvWindow=5000)
	order = request(client,'get',uri,True,data=params)
	qty = -1
	for balance in order['balances']:
		if balance["asset"] == symbol:
			qty = balance["free"]
	return qty

def getAccount(client, recvWindow = 5000):
	params = {
		'recvWindow': recvWindow
	}
	signed = True
	uri = client._create_api_uri('account', True)
	return request(client,'get',uri,signed,data=params)

# override library _request method
def request(client, method, uri, signed, force_params=False, **kwargs):
	data = kwargs.get('data', None)
	if data and isinstance(data, dict):
		kwargs['data'] = data
	if signed:
		# generate signature
		server_time = client.get_server_time()
		kwargs['data']['timestamp'] = server_time['serverTime']
		kwargs['data']['signature'] = client._generate_signature(kwargs['data'])
	if data and (method == 'get' or force_params):
		kwargs['params'] = client._order_params(kwargs['data'])
		del(kwargs['data'])
	response = getattr(client.session, method)(uri, **kwargs)
	return client._handle_response(response)
