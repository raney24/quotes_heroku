from django import forms
from django.forms import widgets
from .models import Stock, UserProfile
from django.contrib.auth.models import User

class StockForm(forms.ModelForm):
	class Meta:
		model = Stock
		exclude = ("submitter", "current_price", "full_title", "projected_er_date")

	def clean_name(self):
		return self.cleaned_data["symbol"].upper()

class AutoCreateStock(forms.ModelForm):
	class Meta:
		model = Stock
		# exclude = ("submitter", "current_price", "full_title", "projected_er_date")
		fields = "__all__"
	def clean_name(self):
		return self.cleaned_data["symbol"].upper()

class UserForm(forms.ModelForm):
	username = forms.CharField(required=True, initial='Username')
	password = forms.CharField(required=True, widget=widgets.PasswordInput(attrs={'class':'input'}), label='Password')
	password2 = forms.CharField(required=True, widget=widgets.PasswordInput(attrs={'class':'input'}), label='Password Again')
	aggressive = forms.BooleanField(widget=forms.CheckboxInput)
	class Meta:
		model = UserProfile
		fields = ('username', 'password', 'aggressive')
	# 	fields = '__all__'

class UserProfileForm(forms.ModelForm):
	# template_name = "registration/registration_form.html"

	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=widgets.PasswordInput(attrs={'class':'input'}), label='Password')
	password2 = forms.CharField(required=True, widget=widgets.PasswordInput(attrs={'class':'input'}), label='Password Again')
	aggressive = forms.BooleanField(widget=forms.CheckboxInput, label='Aggressive?')
	class Meta:
		model = User
		fields = ('username', 'password', 'aggressive')
		# fields = '__all__'



