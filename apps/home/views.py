from django.shortcuts import render, redirect, reverse, HttpResponse
from .models import *
from .forms import ImageUploadForm
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def dummy(request):

    return redirect(reverse('home:index'))

def new_product(request):
    context = {
            "categories": Category.objects.all(),
            "subcategories": Subcategory.objects.all(),
    }
    return render(request, 'home/new_product.html', context)

def add_product(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        subcategory = Subcategory.objects.get(subcategory=request.POST["subcategory"])
        price = request.POST["price"]
        list_price = request.POST["list_price"]
        active = request.POST["active"]
        daily_deal = request.POST["daily_deal"]
        quantity = request.POST["quantity"]
        expire_date = datetime.strptime(request.POST["expire_date"], "%m/%d/%Y")
        product = Product.objects.create(name=name, description=description, subcategory=subcategory, price=price, list_price=list_price, active=active, daily_deal=daily_deal, quantity=quantity, expire_date=expire_date, rating=3)

        return redirect(reverse('home:new_image', kwargs={'id':product.id}))
    else:
        return redirect(reverse('home:new_product'))

def new_image(request, id):
    product = Product.objects.get(id=id)
    context = {
            "product":product
    }
    return render(request, 'home/new_image.html', context)

def upload_image(request, id):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            product = Product.objects.get(id=id)
            m = Image.objects.create(product=product, image = form.cleaned_data['image'])
            return HttpResponse('image upload success')
    return redirect(reverse('home:new_image', kwargs={'id':id}))
