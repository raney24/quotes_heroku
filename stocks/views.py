from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import UpdateView, CreateView, UpdateView, DeleteView
from .models import Stock, Earnings, UserProfile
from django.contrib.auth.models import User
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
from .serializers import StockSerializer, EarningsSerializer#, UserSerializer
from rest_framework.decorators import api_view
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


# class APIUserList(generics.ListAPIView):
# 	queryset = User.objects.all()
# 	serializer_class = UserSerializer

# class APIUserDetail(generics.RetrieveAPIView):
# 	queryset = UserProfile.objects.all()
# 	serializer_class = UserSerializer

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
			# print before_price, after_price
			if before_price == 0 and after_price == 0:
				er_quarter = get_er_quarter(er_date)
				er = Earnings(before_price = before_price,
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

	def get_success_url(self):
		return reverse("profile", kwargs={'slug': self.request.user})

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



# @api_view(['GET', 'POST', ])
# @login_required
# @csrf_exempt
# def stock_collection(request, format=None):
# 	if request.method == 'GET':
# 		stocks = Stock.objects.all()
# 		serializer = StockSerializer(stocks, many=True)
# 		return Response(serializer.data)
# 	elif request.method == 'POST':
# 		serializer = StockSerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def stock_element(request, pk, format=None):
# 	try:
# 		stock = Stock.objects.get(pk=pk)
# 	except Stock.DoesNotExist:
# 		return HttpResponse(status=404)

# 	if request.method == 'GET':
# 		serializer = StockSerializer(stock)
# 		return Response(serializer.data)

# 	elif request.method == 'PUT':
# 		serializer = StockSerializer(stock, data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		return Response(status=status.HTTP_204_NO_CONTENT)








