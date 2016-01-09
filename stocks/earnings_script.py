from datetime import date, timedelta
import datetime
import ystockquote

def prev_weekday(date):
	date -= timedelta(1)
	while date.weekday() > 4:
		date -= timedelta(1)
	return date

def next_weekday(date):
	date += timedelta(1)
	if date.weekday() == 5:
		date += timedelta(3)
	return date

def get_high_prices(symbol, date):
	# date = datetime.date(2015, 10, 21)
	day_before = prev_weekday(date)
	day_after = next_weekday(date)
	# print day_after
	# print date.today()
	if day_after == date.today() or day_after == date.today() - timedelta(1):
		return (0, 0)
	price = ystockquote.get_historical_prices(symbol, str(day_before), str(day_after))
	day_before_price = price[str(day_before)]['High']
	day_after_price = price[str(day_after)]['High']
	# print "daybefore: ", day_before_price
	return (float(day_before_price), float(day_after_price))

def get_er_quarter(date):
	if date.month < 4:
		q = "Q1"
	elif date.month < 7:
		q = "Q2"
	elif date.month < 10:
		q = "Q3"
	else:
		q = "Q4"
	return q

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

