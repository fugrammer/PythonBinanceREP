from binance.enums import *
from operator import itemgetter


class MAGenerator:
	def __init__(self, client, symbol, ma_durations=[7, 25, 99], interval=KLINE_INTERVAL_15MINUTE):
		self.client = client
		self.ma_duration = ma_durations
		self.candles = self.client.get_klines(symbol=symbol, interval=interval)
		self.mas = [[], [], []]
		self.candles = self.candles[len(self.candles) - self.ma_duration[-1]:]
		self.candles_length = len(self.candles)
		self.candles = sorted(self.candles, key=itemgetter(0), reverse=True)
		# Generate MAs
		for i in range(0, len(self.ma_duration)):
			self.mas[i] = [0] * self.ma_duration[i]
		for i in range(0, len(self.candles)):
			for idx, dur in enumerate(self.ma_duration):
				if i < dur:
					average = 0
					for o in range(1, 5):
						average += float(self.candles[i][o])
					average /= 4
					self.mas[idx][i] = average

	def update(self, average):
		for idx, ma in enumerate(self.mas):
			self.mas[idx] = ma[1:]
			self.mas[idx].insert(0, average)

	def get_mas(self):
		result = {}
		for idx, MA in enumerate(self.mas):
			average = sum(self.mas[idx]) / len(self.mas[idx])
			result[idx] = average
		return result
