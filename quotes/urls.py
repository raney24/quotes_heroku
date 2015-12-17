from django.conf.urls import patterns, include, url
from django.contrib import admin
from stocks.views import *
# from stocks.views import MyView
from stocks import views
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import routers
admin.autodiscover()

# router = routers.DefaultRouter()
# router.register(r'stocks', StockViewSet)


urlpatterns = patterns('',

	url(r'^admin/', include(admin.site.urls)),

	url(r'^$', StockListView.as_view(), name='home'),

	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name="login"),

	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),

	url(r'^accounts/', include('registration.backends.simple.urls')),

	url(r'^users/(?P<slug>\w+)/$', UserProfileDetailView.as_view(), name="profile"),

	url(r'^edit_profile/$', login_required(UserProfileEditView.as_view()), name="edit_profile"),

	url(r'^stock/create/$', StockCreateView.as_view(), name='stock_create'),

	# url(r'^stock/(?P<pk>\d+)/$', StockDetailView.as_view(), name='stock_detail'),

	url(r'^stock/er/(?P<pk>\d+)/$', EarningsReportView.as_view(template_name="earnings_detail.html"), name='stock_er_detail'),

	# (r'^about/', MyView.as_view()),

	url(r'^stock/update/(?P<pk>\d+)/$', login_required(StockUpdateView.as_view()), name='stock_update'),

	url(r'^stock/delete/(?P<pk>\d+)/$', login_required(StockDeleteView.as_view()), name='stock_delete'),

	#user auth
	url(r'^logout/$', 'django.contrib.auth.views.logout', { 'next_page':"/" }),

	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api/v1/stocks/$', views.APIStockList.as_view()),
	url(r'^api/v1/stocks/(?P<pk>[0-9]+)$', views.APIStockDetail.as_view()),	

	url(r'^api/v1/earnings/$', views.APIEarningsList.as_view()),
	# url(r'^api/v1/users/$', views.APIUserList.as_view()),
	# url(r'^api/v1/users/(?P<pk>[0-9]+)$', views.APIUserDetail.as_view()),	
	# url(r'^', include(router.urls)),
	

	# url(r'^(?P<pk>[0-9]+)/$', views.index, name='test'),
    # Examples:
    # url(r'^$', 'quotes.views.home', name='home'),
    # url(r'^quotes/', include('quotes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

#REST URLS
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = format_suffix_patterns(urlpatterns)
