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

			super(Stock, self).save(**kwargs)
		except IntegrityError as e:
			return render_to_response("stocks/stock_form.html", {"message": e.message})

	def create(self, **kwargs):
		self.symbol = self.symbol.upper()

		self.full_title = get_stock_title(self.symbol)
		pd = get_projected_er_date(self.symbol)
		self.projected_er_date = pd

		super(Stock, self).save(**kwargs)

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

	def __unicode__(self):
		return self.stock

	# def get_absolute_url(self):
	# 	return reverse("earnings", kwargs={"pk": str(self.id)})

class UserProfile(models.Model):
	user = models.OneToOneField(User, unique=True)
	aggressive = models.BooleanField(default=False)

	# objects = UserProfileManager()

	def __unicode__(self):
		return "%s's profile" % self.user





