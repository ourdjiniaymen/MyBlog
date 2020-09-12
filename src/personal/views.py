from django.shortcuts import render
from account.models import Account

def home_screen_view(request):
    context = {}
    context['accounts'] = Account.objects.all()
    return render(request,'personal/home.html',context)#render(request,reference,context//data or variables)"""