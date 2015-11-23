from django.db import models
from django.db.models import Count
from django.core.urlresolvers import reverse
import ystockquote

class Stock(models.Model):
	symbol = models.CharField("Stock Symbol", max_length=5)
	submitted_on = models.DateTimeField(auto_now_add=True)
	# notes = models.TextField(blank=True)
	last_accessed = models.DateTimeField(auto_now_add=True)
	# current_price = models.DecimalField(max_digits = 10, decimal_places=2)

	objects = models.Manager()

	def last_er(self):
		return self.earnings_set.order_by(id).last()

	def __unicode__(self):
		return self.symbol

	def get_absolute_url(self):
		return reverse("stock_detail", kwargs={"pk": str(self.id)})

class Earnings(models.Model):
	stock = models.ForeignKey(Stock)
	before_price = models.DecimalField(max_digits=10, decimal_places=2)
	after_price = models.DecimalField(max_digits=10, decimal_places=2)
	er_date = models.DateField()
	er_quarter = models.TextField(default="Q1")
	# er_date = models.CharField(max_length=10, )

	def __unicode__(self):
		return self.stock

	# def get_absolute_url(self):
	# 	return reverse("earnings", kwargs={"pk": str(self.id)})






