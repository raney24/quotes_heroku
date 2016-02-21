from django.db import models
from django.db.models import Count
from django.core.urlresolvers import reverse
import ystockquote
from scraper import *
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render_to_response
from scraper import *
from earnings_script import *

class Stock(models.Model):
	symbol = models.CharField("Stock Symbol", max_length=5, unique=True)
	full_title = models.CharField("Stock Name", max_length=40, default="Unknown Stock")
	submitted_on = models.DateTimeField(auto_now_add=True)
	submitter = models.ForeignKey('auth.User', blank=True)
	# notes = models.TextField(blank=True)
	last_accessed = models.DateTimeField(auto_now_add=True)
	projected_er_date = models.DateField(default="2000-1-1")

	objects = models.Manager()

	def save(self, **kwargs):
		try: 
			self.symbol = self.symbol.upper()

			self.full_title = get_stock_title(self.symbol)

			pd = get_projected_er_date(self.symbol)
			self.projected_er_date = get_projected_er_date(self.symbol)
			print "About to create er"
			# super(Earnings, self).create(self.symbol)
			
			super(Stock, self).save(**kwargs)
			er = Earnings()
			er.create(self.symbol)
			
		except IntegrityError as e:
			return render_to_response("stocks/stock_form.html", {"message": e.message})

	# def create(self, **kwargs):
	# 	self.symbol = self.symbol.upper()

	# 	self.full_title = get_stock_title(self.symbol)
	# 	pd = get_projected_er_date(self.symbol)
	# 	self.projected_er_date = pd
		
	# 	super(Stock, self).save(**kwargs)
	# 	print "About to create er"
	# 	super(Earnings, self).create(self.symbol)

	def last_er(self):
		return self.earnings_set.order_by(id).last()

	def __unicode__(self):
		return self

	def get_absolute_url(self):
		return reverse("stock_detail", kwargs={"pk": str(self.id)})

class Earnings(models.Model):
	stock = models.ForeignKey(Stock)
	before_price = models.DecimalField(max_digits=10, decimal_places=2)
	after_price = models.DecimalField(max_digits=10, decimal_places=2)
	er_date = models.DateField()
	er_quarter = models.TextField(default="Q1")
	percent_change = models.DecimalField(max_digits=11, decimal_places=2, null=True)

	def create(self, symbol):
		# stock = super(Stock, self).get_object()
		er_dict = get_earnings_reports(symbol)
		for key in er_dict:
			er_date = datetime.datetime.strptime(key, '%m/%d/%Y').date()
			before_price, after_price = get_high_prices(symbol, er_date)
			# print before_price, after_price
			if before_price == 0 and after_price == 0:
				er_quarter = get_er_quarter(er_date)
				er = Earnings(
								before_price = before_price,
								after_price = after_price, 
								er_date = er_date, 
								er_quarter = er_quarter,
								percent_change = 0,
							)
				er.stock = stock
				er.save()
				return stock

			er_quarter = get_er_quarter(er_date)
			percent_change = float(before_price - after_price) / before_price*(-1) * 100
			percent_change = round(percent_change, 2)

			er = Earnings(before_price = before_price, 
							after_price = after_price, 
							er_date = er_date, 
							er_quarter = er_quarter,
							percent_change = percent_change,
							)
			# s = Stock.objects.get(symbol="TWTR")
			# er.stock = s

			if not Earnings.objects.filter(er_quarter = er.er_quarter, stock_id = er.stock_id).exists():
				er.save()
		stock.projected_er_date = get_projected_er_date(stock.symbol)

	def __unicode__(self):
		return self.stock

class UserProfile(models.Model):
	user = models.OneToOneField(User, unique=True)
	aggressive = models.BooleanField(default=False)

	# objects = UserProfileManager()

	def __unicode__(self):
		return "%s's profile" % self.user





