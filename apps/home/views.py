from django.shortcuts import render, redirect, reverse
from .models import *

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def dummy(request):

    return redirect(reverse('home:index'))

def add_product(request):

    context = {
            "categories": Category.objects.all(),
            "subcategories": Subcategory.objects.all(),
    }
    return render(request, 'home/add_product.html')
