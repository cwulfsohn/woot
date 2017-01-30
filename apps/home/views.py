from django.shortcuts import render, redirect, reverse
from .models import *

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def dummy(request):
    subcategory = Subcategory.objects.get(subcategory="Laptops")
    Product.objects.create(name="Macbook Pro", description="Overpriced, but sexy as hell.", price=999.99, list_price=1299.99, rating=5, active=True, daily_deal=False, quantity=300, subcategory=subcategory)

    return redirect(reverse('home:index'))
