from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import UpdateView, CreateView, UpdateView, DeleteView
from .models import Stock, Earnings, UserProfileManager, UserProfile
from .forms import  StockForm
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
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
		er_dict = get_earnings_reports(stock.symbol)
		for key in er_dict:
			er_date = datetime.datetime.strptime(key, '%m/%d/%Y').date()
			before_price, after_price = get_high_prices(stock.symbol, er_date)
			er_quarter = get_er_quarter(er_date)
			er = Earnings(before_price = before_price, after_price = after_price, er_date = er_date, er_quarter = er_quarter)
			er.stock = stock
			if not Earnings.objects.filter(er_quarter = er.er_quarter, stock_id = er.stock_id).exists():
				print er.er_date
				er.save()
		return stock


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

def user_profile(request, username):
	user = get_object_or_404(User, username=username)
	profile = UserProfile.objects.get(user=user)

	return render(request, 'public/profile.html', {'profile': profile})

# def login(request):
# 	return render(request, 'login.html')

# @login_required(login_url='/')
# def home(request):
# 	return render_to_response('home.html')

# def logout(request):
# 	auth_logout(request)
# 	return redirect('/')











