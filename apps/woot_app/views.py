from django.shortcuts import render, redirect

def index(request):
    return render(request, 'woot_app/index.html')
# Create your views here.
