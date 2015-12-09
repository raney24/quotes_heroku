from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import UpdateView, CreateView, UpdateView, DeleteView
from .models import Stock, Earnings, UserProfile
from .forms import  StockForm, UserForm, UserProfileForm
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
	success_url = "/"

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
			diff = before_price - after_price
			if before_price > after_price:
				percent_sign = -1
			else:
				percent_sign = 1
			percent_change = (diff / before_price * 100) * percent_sign
			print percent_change
			er = Earnings(before_price = before_price, 
							after_price = after_price, 
							er_date = er_date, 
							er_quarter = er_quarter,
							percent_change = percent_change)
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

class StockUpdateView(UpdateView):
	model = Stock
	form_class = StockForm

class StockDeleteView(DeleteView):
	model = Stock
	success_url = "/"

	# template_name = 'delete_note.html'

class UserProfileDetailView(DetailView):
	model = get_user_model()
	slug_field = "username"
	template_name = "user_detail.html"

	def get_object(self, queryset=None):
		user = super(UserProfileDetailView, self).get_object(queryset)
		UserProfile.objects.get_or_create(user=user)
		return user

class UserProfileEditView(UpdateView):
	model = UserProfile
	form_class = UserProfileForm
	template_name = "edit_profile.html"

	def get_object(self, queryset=None):
		return UserProfile.objects.get_or_create(user = self.request.user)[0]

	# def get_success_url(self):
	# 	return reverse("profile", kwargs={'slug': self.request.user})

@login_required
def user_profile(request, username):
	user = get_object_or_404(User, username=username)
	profile = UserProfile.objects.get(user=user)

	return render(request, 'user_detail.html', {'profile': profile})

from django.template.defaulttags import register
from .forms import UserForm
def register(request):
    user_form = UserForm()
    if request.user.is_authenticated():
        
        return render(request, 'public/register.html', {'form': user_form})

    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            this_user = UserProfile()
            this_user.user = user
            this_user.save()
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            login(request, user)
            return redirect('stock_list.html')

    return render(request, 'public/register.html', {'form': user_form})












