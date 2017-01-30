from django.shortcuts import render, redirect, reverse
from .models import *

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def dummy(request):
    
    return redirect(reverse('home:index'))
