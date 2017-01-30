from django.shortcuts import render, redirect, reverse
from .models import *

def index(request):
    return render(request, 'discussions/index.html')

def dummy(request):
    
    return redirect(reverse('home:dummy'))
