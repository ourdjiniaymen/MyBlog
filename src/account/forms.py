from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate


from account.models import Account



class UserRegistrationForm(UserCreationForm):
	#without this, there is no help text in the email field
	email					= forms.EmailField(max_length=60, help_text="Required. Add a valid email address")

	class Meta:
		model = Account
		fields = ('email','username','password1','password2')

class AccountAuthentificationForm(forms.ModelForm):
	#without this, the password field will be just a text field
	password 				= forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email','password')


	def clean(self):
		""" this method is availabe in any form that extands the Model.form
	    		it is like an interceptor,before the form can do anything it has to run it"""
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			#if the email or the passoword is wrong , we must attach a validation error to the form
			#this is a non-field error
			if not authenticate(email=email,password=password):
				raise forms.ValidationError("Invalid login")
	

class AccountUpdateForm(forms.ModelForm):
	
	class Meta:
		model = Account
		fields = ('email','username')

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError("Email '%s' is alredy in use" % email)

	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
			except Account.DoesNotExist:
				return username
			raise forms.ValidationError("Username '%s' is alredy in use" % username)
		