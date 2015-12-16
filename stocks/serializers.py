from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class StockSerializer(serializers.ModelSerializer):
	class Meta:
		model = Stock
		fields = '__all__'
		# fields = ('pk', 'symbol', 'submitted_on', 'submitter', 'last_accessed', 'projected_er_date')

	submitter = serializers.ReadOnlyField(source='submitter.username')
	projected_er_date = serializers.ReadOnlyField()
	full_title = serializers.ReadOnlyField()


class UserSerializer(serializers.ModelSerializer):
	stock = serializers.PrimaryKeyRelatedField(many=True, queryset=Stock.objects.all())

	class Meta:
		model = User
		fields = ('id', 'username', 'stocks')
		