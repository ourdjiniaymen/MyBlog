from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from account.forms import UserRegistrationForm


def registration_view(request):
	context = {}
	if request.POST:
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request,account)
			return redirect('home')
		else:
			context['registration_form'] = form
	else: #GET_request / load the page for the first time
		form =UserRegistrationForm()
		context['registration_form'] = form
	return render(request,'account/register.html',context)