from django.shortcuts import render, redirect, reverse, HttpResponse
from .models import *
from .forms import ImageUploadForm
from datetime import datetime
from django.contrib import messages

# Create your views here.
def index(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    context = {'categories': categories,
               'subcategories': subcategories
               }
    return render(request, 'home/index.html', context)

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
        expire_date = request.POST["expire_date"]
        errors = Product.objects.validate(name,description,price,list_price,quantity,expire_date)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(reverse('home:new_product'))
        expire_date = datetime.strptime(expire_date, "%m/%d/%Y")
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
            image = Image.objects.create(product=product, image = form.cleaned_data['image'])
            return redirect(reverse('home:features', kwargs={'id':id}))
    print "failure"
            return redirect(reverse('home:show_product', kwargs={'id':id}))
    return redirect(reverse('home:new_image', kwargs={'id':id}))

def category(request):
    pass

def show_product(request, id):
    # try:
    product = Product.objects.get(id=id)
    images = Image.objects.filter(product=product)
    for image in images:
        image.image.name = image.image.name[17:]
    context = {
                "product":product,
                "images":images
    }
    return render(request, 'home/show.html', context)
    # except:
    #     return redirect(reverse('home:index'))

def features(request, id):
    product = Product.objects.get(id=id)
    features = Feature.objects.filter(product = id).order_by("-created_at")
    context = {
        'product':product,
        'features':features
    }
    return render(request, "home/features.html", context)

def add_feature(request, id):
    if request.method == 'POST':
        feature_header = request.POST['feature_header']
        feature_description = request.POST['feature_description']
        product = Product.objects.get(id=id)
        Feature.objects.create(header = feature_header, feature = feature_description, product = product)
    return redirect(reverse('home:features', kwargs={'id':id}))

def delete_feature(request, id, feature_id):
    delete_feature = Feature.objects.get(id=feature_id)
    delete_feature.delete()
    return redirect(reverse('home:features', kwargs={'id':id}))

def specifications(request, id):
    return render(request, "home/spec.html")

def add_specification(request, id):
    if request.method == 'POST':
        feature_header = request.POST['feature_header']
        feature_description = request.POST['feature_description']
        product = Product.objects.get(id=id)
        Feature.objects.create(header = feature_header, feature = feature_description, product = product)
    return redirect(reverse('home:features', kwargs={'id':id}))

def delete_specification(request, id, feature_id):
    delete_feature = Feature.objects.get(id=feature_id)
    delete_feature.delete()
    return redirect(reverse('home:features', kwargs={'id':id}))
