from .models import *
from rest_framework import serializers

class StockSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Stock
		fields = ('symbol', 'submitted_on', 'submitter', 'last_accessed')
		