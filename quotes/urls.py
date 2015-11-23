from django.conf.urls import patterns, include, url
from django.contrib import admin
from stocks.views import StockListView, StockCreateView, StockDetailView, StockDeleteView, StockUpdateView,  EarningsReportView
# from stocks.views import MyView
from stocks import views
from django.contrib.auth.decorators import login_required as auth
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',


	url(r'^admin/', include(admin.site.urls)),

	url(r'^$', StockListView.as_view(), name='home'),

	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name="login"),

	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),

	url(r'^accounts/', include('registration.backends.simple.urls')),


	url(r'^stock/create/$', StockCreateView.as_view(), name='stock_create'),

	url(r'^stock/(?P<pk>\d+)/$', StockDetailView.as_view(), name='stock_detail'),

	url(r'^stock/er/(?P<pk>\d+)/$', EarningsReportView.as_view(template_name="earnings_detail.html"), name='stock_er_detail'),

	# (r'^about/', MyView.as_view()),

	url(r'^stock/update/(?P<pk>\d+)/$', auth(StockUpdateView.as_view()), name='stock_update'),

	url(r'^stock/delete/(?P<pk>\d+)/$', auth(StockDeleteView.as_view()), name='stock_delete'),

	# url(r'^(?P<pk>[0-9]+)/$', views.index, name='test'),
    # Examples:
    # url(r'^$', 'quotes.views.home', name='home'),
    # url(r'^quotes/', include('quotes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
