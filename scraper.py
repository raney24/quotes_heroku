from bs4 import BeautifulSoup
import urllib2
from urllib2 import Request, urlopen

import re
from datetime import datetime
# import datetime
import dateutil.parser as dparser

def get_potential_stocks(current_stocks):
	sgi_url = "http://sgi.seleritycorp.com/category/north-america/"
	# proxy_handler = urllib2.ProxyHandler({'http': 'http://sgi.seleritycorp.com/category/north-america/'})
	req = urllib2.Request(sgi_url, headers={'User-Agent' : 'Magic Browser'})
	# opener = urllib2.urlopen(req)
	r = urlopen(req).read()
	soup = BeautifulSoup(r, "html.parser")
	stock_symbol = soup.find_all("h2", { "class" : "subheader" }, limit=10)
	upcoming_er_array = []
	for s in stock_symbol:
		s = str(s.get_text())
		s = s[s.find("(")+1:s.find(")")]
		upcoming_er_array.append(s)

	return upcoming_er_array

def get_soup(symbol):
	nasURL = 'http://www.nasdaq.com/earnings/report/'
	symbolLower = symbol.lower()
	proxy_handler = urllib2.ProxyHandler({'http': 'http://www.nasdaq.com/earnings/report/' + symbolLower})
	opener = urllib2.build_opener(proxy_handler)
	r = opener.open('http://www.nasdaq.com/earnings/report/' + symbolLower)
	soup = BeautifulSoup(r, "html.parser")
	return soup

def get_stock_title(symbol):
	soup = get_soup(symbol)
	title = soup.find("title")
	title = str(title.get_text())
	title = title.partition("(")[0]
	return title

def get_projected_er_date(symbol):
	soup = get_soup(symbol)
	er_projection = soup.find("span", { "id" : "two_column_main_content_reportdata" })
	er_projection = str(er_projection.get_text())
	match = re.search(r'(\d+/\d+/\d+)', er_projection)
	if match:
		d = match.group(1)
		d = datetime.strptime(d, '%m/%d/%Y').strftime('%Y-%m-%d')
	else: 
		d = "2000-1-1"
	return d

def get_earnings_reports(symbol):
	soup = get_soup(symbol)
	letters = soup.find_all("div", class_="genTable")
	tr = letters[0].find_all("td")

	earnings_reports = {}

	tr[1] = tr[1].get_text()
	tr[2] = tr[2].get_text()
	tr[6] = tr[6].get_text()
	tr[7] = tr[7].get_text()
	tr[11] = tr[11].get_text()
	tr[12] = tr[12].get_text()
	tr[16] = tr[16].get_text()
	tr[17] = tr[17].get_text()

	dateElementArray = [1, 6, 11, 16]

	# earnings_reports = {
	# 	"Q1" : 1,
	# 	"Q2" : 1,
	# 	"Q3" : 1,
	# 	"Q4" : 1
	# }

	for i in dateElementArray:
		if int(tr[i][0:2]) < 4: 
			earnings_reports[tr[i]] = tr[i+1]
		elif int(tr[i][0:2]) < 7:
			earnings_reports[tr[i]] = tr[i+1]
		elif int(tr[i][0:2]) < 10:
			earnings_reports[tr[i]] = tr[i+1]
		else:
			earnings_reports[tr[i]] = tr[i+1]

	return earnings_reports
