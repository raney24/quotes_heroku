from django import forms
from .models import Stock, UserProfile
from django.contrib.auth.models import User

class StockForm(forms.ModelForm):
	class Meta:
		model = Stock
		exclude = ("submitter", "current_price", "full_title", "projected_er_date")

	def clean_name(self):
		return self.cleaned_data["symbol"].upper()

class UserForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		# fields = ('username', 'password')
		fields = '__all__'

class UserProfileForm(forms.ModelForm):
	aggressive = forms.BooleanField(widget=forms.CheckboxInput)
	class Meta:
		model = UserProfile
		# fields = ('username', 'password')
		fields = '__all__'
