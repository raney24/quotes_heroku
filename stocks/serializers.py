from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class StockSerializer(serializers.ModelSerializer):
	class Meta:
		model = Stock
		fields = '__all__'
		# fields = ('pk', 'symbol', 'submitted_on', 'submitter', 'last_accessed', 'projected_er_date')

	# def __init__(self, *args, **kwargs):
	# 	symbol = request.symbol
	# 	super(StockSerializer, self).__init__(symbol=symbol, *args, **kwargs)

	submitter = serializers.ReadOnlyField(source='submitter.username')
	projected_er_date = serializers.ReadOnlyField()
	full_title = serializers.ReadOnlyField()

class EarningsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Earnings
		fields = '__all__'

	def __unicode__(self):
		return self.Earnings

# class UserSerializer(serializers.ModelSerializer):
# 	stock = serializers.PrimaryKeyRelatedField(many=True, queryset=Stock.objects.all())

# 	class Meta:
# 		model = UserProfile
# 		fields = ('id', 'username', 'stock')

		