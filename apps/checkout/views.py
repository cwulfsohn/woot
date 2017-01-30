from django.shortcuts import render, redirect, reverse

def index(request):
    return render(request, 'checkout/index.html')
