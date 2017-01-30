from django.shortcuts import render, redirect, reverse
from .models import *

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def dummy(request):
    category = Category.objects.get(category="Home & Kitchen")
    Subcategory.objects.create(subcategory="Bath", category=category)

    return redirect(reverse('home:index'))
