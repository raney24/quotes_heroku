from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.base import View
from django.views.generic.edit import UpdateView, CreateView, UpdateView, DeleteView, FormView
from .models import Stock, Earnings, UserProfile
from django.contrib.auth.models import User
from .forms import  *
from django.contrib.auth import get_user_model, authenticate
from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from datetime import datetime
from datetime import date, timedelta
from earnings_script import ER_Stock
from scraper import *
from earnings_script import *
from .serializers import StockSerializer, EarningsSerializer#, UserSerializer
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from stocks.permissions import IsOwnerOrReadOnly
import ystockquote
import datetime

class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

class APIStockList(generics.ListCreateAPIView):
	queryset = Stock.objects.all()
	serializer_class = StockSerializer

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def perform_create(self, serializer):
		serializer.save(submitter=self.request.user)

class APIStockDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Stock.objects.all()
	serializer_class = StockSerializer

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
							IsOwnerOrReadOnly, )

class APIEarningsList(generics.ListAPIView):
	queryset = Earnings.objects.all()
	serializer_class = EarningsSerializer

class APIEarningsDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Earnings.objects.filter(stock = 1)
	serializer_class = EarningsSerializer

class APIStockEarningsDetail(generics.ListAPIView):
	serializer_class = EarningsSerializer
	def get_queryset(self):
		stock_id = self.kwargs['pk']
		return Earnings.objects.filter(stock=stock_id)


# class APIUserList(generics.ListAPIView):
# 	queryset = User.objects.all()
# 	serializer_class = UserSerializer

# class APIUserDetail(generics.RetrieveAPIView):
# 	queryset = UserProfile.objects.all()
# 	serializer_class = UserSerializer

class StockListView(ListView):
	model = Stock
	context_object_name = 'stock_symbols'
	current_stocks = Stock.objects.all()
	form_class = StockForm

	def get_context_data(self, **kwargs):
		context = super(StockListView, self).get_context_data(**kwargs)
		context['er_list'] = get_potential_stocks(self.current_stocks)
		return context

def quick_add_stock(request, symbol):
	stock = Stock(symbol=symbol, submitter=request.user)
	stock.objects.create_stock()
	print stock.full_title
	return redirect("home")

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
			er.stock = stock

			if not Earnings.objects.filter(er_quarter = er.er_quarter, stock_id = er.stock_id).exists():
				er.save()
		stock.projected_er_date = get_projected_er_date(stock.symbol)
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

class AutoCreateStock(View):
	# model = Stock
	# success_url = "/"
	def get(request, *args, **kwargs):
		Stock(symbol="AAPL", submitter=2).save()
		return HttpResponse("/")

class UserProfileDetailView(DetailView):
	model = get_user_model()
	slug_field = "username"
	template_name = "user_detail.html"

	def get_object(self, queryset=None):
		user = super(UserProfileDetailView, self).get_object(queryset)
		user = UserProfile.objects.get_or_create(user=user)
		print user
		return user

class UserDeleteView(DeleteView):
	model = User
	success_url = '/'

class AccountRegistrationView(FormView):
	template_name = 'registration/registration_form.html'
	form_class = UserForm

	def form_valid(self, form):
		AccountRegistrationView.register_user(self.request, **form.cleaned_data)
		return super(AccountRegistrationView, self).form_valid(self, form)

	def get_context_data(self, **kwargs):
		context = super(AccountRegistrationView, self).get_context_data(**kwargs)
		context.update(self.extra_context)


from django.template.defaulttags import register
from .forms import UserProfileForm
def register(request):
    template = "registration/registration_form.html"
    user_form = UserProfileForm()
    if request.user.is_authenticated():
        
        return render(request, 'registration/registration_form.html', {'form': user_form})

    if request.method == "POST":
        user_form = UserProfileForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            this_user = UserProfile()
            this_user.user = user
            this_user.save()
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            return redirect('stock_list.html')

    return render(request, 'registration/registration_form.html', {'form': user_form})

class UpdateUserProfileView(UpdateView):
	model = User
	slug_field = "username"
	form_class = UserProfileForm
	template_name = 'edit_profile.html'











