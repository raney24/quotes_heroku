from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import UpdateView, CreateView, UpdateView, DeleteView
from .models import Stock, Earnings
from .forms import  StockForm
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import ystockquote
import datetime
from datetime import datetime
from datetime import date, timedelta
from earnings_script import ER_Stock
from scraper import *
from earnings_script import *

class StockListView(ListView):
	model = Stock
	context_object_name = 'stock_symbols'



class StockCreateView(CreateView):
	model = Stock
	form_class = StockForm

	def form_valid(self, form):
		f = form.save(commit=False)
		f.submitter = self.request.user
		f.save()

		return super(CreateView, self).form_valid(form)

from django import template
from django.template.loader import get_template 

class EarningsReportView(DetailView):
	model = Stock

	def get_object(self):
		stock = super(EarningsReportView, self).get_object()
		# stock.prefetch_related()	
		stockHelper = ER_Stock(stock.symbol)
		stockHelper.get_high_prices(date)
		er_dict = get_earnings_reports(stock.symbol)
		dt = datetime.datetime.strptime(er_dict.keys()[1], '%m/%d/%Y').date()
		print dt
		# stockHelper.get_er_quarter(date)
		er = Earnings(before_price = stockHelper.day_before_price, after_price = stockHelper.day_after_price, er_date = dt)
		er.stock = stock
		print stockHelper.day_before_price, stockHelper.day_after_price, er.er_date
		print er.stock_id
		
		# if not Earnings.objects.filter().exists():
			# print "asDasdasd"
		er.save()
		return stock

	# def get_object(self):
	# 	stock = super(EarningsReportView, self).get_object()
	# 	er_dict = get_earnings_reports(stock.symbol)
	# 	dt = datetime.datetime.strptime(er_dict.keys()[1], '%m/%d/%Y').date()
	# 	before_price, after_price = get_high_prices(stock.symbol, dt)
	# 	print before_price, after_price, dt
	# 	er = Earnings(before_price = before_price, after_price = after_price, er_date = dt)
	# 	if not Earnings.objects.filter(er_date = er.er_date, stock_id = er.stock_id).exists():
	#  		er.save()
	#  	return stock

	# def get_object(self):
	# 	stock = super(EarningsReportView, self).get_object()
	# 	# stock.prefetch_related()	
	# 	stockHelper = ER_Stock(stock.symbol)
	# 	stockHelper.get_high_prices(date)
	# 	er = Earnings(before_price = stockHelper.day_before_price, after_price = stockHelper.day_after_price)
	# 	er.stock = stock
	# 	er.save()
	# 	return stock
	# context_object_name = 'stock_earnings'

class StockDetailView(DetailView):
	model = Stock

	

	def get_objects(self, queryset=None):
		stock = super(StockDetailView, self).get_object(queryset)
		Stock.objects.get_object(stock=stock)
		return stock

	def get_context_data(self, **kwargs):
		
		context = super(StockDetailView, self).get_context_data(**kwargs)

		context['stock_list'] = Stock.objects.all()
		# print context
		return context

# class MyView(View)
# 	def get(self, request):
# 		return HttpResponse('Hello')

class StockUpdateView(UpdateView):
	model = Stock
	form_class = StockForm

class StockDeleteView(DeleteView):
	model = Stock
	success_url = reverse_lazy("home")











