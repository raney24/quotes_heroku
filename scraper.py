from bs4 import BeautifulSoup
import urllib2
import re

def get_earnings_reports(symbol):
	nasURL = 'http://www.nasdaq.com/earnings/report/'
	symbolLower = symbol.lower()
	proxy_handler = urllib2.ProxyHandler({'http': 'http://www.nasdaq.com/earnings/report/' + symbolLower})
	opener = urllib2.build_opener(proxy_handler)
	r = opener.open('http://www.nasdaq.com/earnings/report/goog')
	soup = BeautifulSoup(r, "html.parser")
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
