from datetime import date, timedelta
import datetime
import ystockquote

def get_high_prices(symbol, date):
	# date = datetime.date(2015, 10, 21)
	day_before = date - timedelta(1)
	day_after = date + timedelta(1)
	price = ystockquote.get_historical_prices(symbol, str(day_before), str(day_after))
	day_before_price = price[str(day_before)]['High']
	day_after_price = price[str(day_after)]['High']
	# print "daybefore: ", day_before_price
	return (float(day_before_price), float(day_after_price))


class ER_Stock(object):
	def __init__(self, symbol):
		self.symbol = symbol
		self.day_before_price = 0
		self.day_after_price = 0
		self.date = '1-1-2010'

	def get_high_prices(self, date):
		date = datetime.date(2015, 10, 21)
		day_before = date - timedelta(1)
		day_after = date + timedelta(1)
		price = ystockquote.get_historical_prices(self.symbol, str(day_before), str(day_after))
		self.day_before_price = price[str(day_before)]['High']
		self.day_after_price = price[str(day_after)]['High']

