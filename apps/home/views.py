from django.shortcuts import render, redirect, reverse, HttpResponse
from .models import *
from .forms import ImageUploadForm
from datetime import datetime
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    today = datetime.now().date()
    daily_deal = Product.objects.get(daily_deal=True, deal_date = today)
    deal_images = Image.objects.filter(product = daily_deal)
    comments = Comment.objects.filter(product = daily_deal).order_by('-created_at')[:2]
    for image in deal_images:
        image.image.name = image.image.name[17:]
    percent_off = Product.objects.percent_off(daily_deal.price, daily_deal.list_price)
    context = {'categories': categories,
               'subcategories': subcategories,
               'daily_deal': daily_deal,
               'deal_image': deal_images,
               'percent_off': percent_off,
               'comments': comments,
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
        category = request.POST["category"]
        sub = str(category) + "_subcategory"
        name = request.POST["name"]
        description = request.POST["description"]
        subcategory = Subcategory.objects.get(id=request.POST[sub])
        print subcategory.subcategory
        price = request.POST["price"]
        list_price = request.POST["list_price"]
        active = request.POST["active"]
        daily_deal = request.POST["daily_deal"]
        quantity = request.POST["quantity"]
        expire_date = request.POST["expire_date"]
        if request.POST["deal_date"]:
            deal_date=request.POST["deal_date"]
        else:
            deal_date=None
        errors = Product.objects.validate(name,description,price,list_price,quantity,expire_date, deal_date)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(reverse('home:new_product'))
        expire_date = datetime.strptime(expire_date, "%m/%d/%Y")
        product = Product.objects.create(name=name, description=description, subcategory=subcategory, price=price, list_price=list_price, active=active, daily_deal=daily_deal, quantity=quantity, expire_date=expire_date, rating=3)
        if deal_date:
            deal_date = datetime.strptime(deal_date, "%m/%d/%Y")
            product.deal_date=deal_date
            product.save()
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
    return redirect(reverse('home:new_image', kwargs={'id':id}))

def category(request, id):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    category = Category.objects.get(id = id)
    this_cat_subcategories = Subcategory.objects.filter(category = category)
    ending_soon = Product.objects.filter(subcategory__category=category).order_by('expire_date')[:4]
    main_product = ending_soon[0]
    images = Image.objects.filter(product=main_product)
    comments = Comment.objects.filter(product = main_product).order_by('-created_at')[:1]
    percent_off = Product.objects.percent_off(main_product.price, main_product.list_price)
    all_products = Product.objects.filter(subcategory__category=category).exclude(id = main_product.id)
    all_images = {}
    for product in all_products:
        many_images = Image.objects.filter(product=product)
        for image in many_images:
            all_images[product.id] = image.image.name[17:]
    for image in images:
        image.image.name = image.image.name[17:]
    context = {'categories': categories,
               'subcategories': subcategories,
               'this_category': category,
               'this_cat_subcategories': this_cat_subcategories,
               'main_product': main_product,
               'images': images,
               'comments': comments,
               'percent_off': percent_off,
               'all_products': all_products,
               'all_images': all_images,
               }
    return render(request, 'home/category.html', context)

def subcategory(request):
    pass

def show_product(request, id):
    # try:
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    product = Product.objects.get(id=id)
    images = Image.objects.filter(product=product)
    comments = Comment.objects.filter(product = product).order_by('-created_at')[:2]
    percent_off = Product.objects.percent_off(product.price, product.list_price)
    for image in images:
        image.image.name = image.image.name[17:]
    context = {'categories': categories,
               'subcategories': subcategories,
               'product': product,
               'images': images,
               'comments': comments,
               'percent_off': percent_off,
               }
    return render(request, 'home/product.html', context)
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
    product = Product.objects.get(id=id)
    specifications = Specifications.objects.filter(product = id).order_by("-created_at")
    categories = SpecificationCategories.objects.all()
    context = {
        'product':product,
        'specifications':specifications,
        'categories':categories,
    }
    return render(request, "home/spec.html", context)

def add_specification(request, id):
    if request.method == 'POST':
        description = request.POST['specification_description']
        if len(description) < 2:
            return redirect(reverse('home:specifications', kwargs={'id':id}))
        try:
            checked =  request.POST['add_spec_header']
            if checked:
                category = request.POST['specification_header']
                SpecificationCategories.objects.create(category = category)
                category_id = SpecificationCategories.objects.get(category = category)
                product = Product.objects.get(id = id)
                Specifications.objects.create(product = product, spec_category=category_id, value=description)
                print "worked"
        except:
            category = request.POST['specification_select']
            if category == "revert":
                return redirect(reverse('home:specifications', kwargs={'id':id}))
            else:
                category_id = SpecificationCategories.objects.get(category = category)
                product = Product.objects.get(id = id)
                Specifications.objects.create(product = product, spec_category=category_id, value=description)
    return redirect(reverse('home:specifications', kwargs={'id':id}))

def delete_specification(request, id, spec_id):
    delete_specification = Specifications.objects.get(id=spec_id)
    delete_specification.delete()
    return redirect(reverse('home:specifications', kwargs={'id':id}))

def discussion(request, id):
    print request.session['id']
    user = User.objects.get(id = request.session["id"])
    product = Product.objects.get(id = id)
    comments = Comment.objects.filter(product=id).order_by("created_at")
    context = {
        'user':user,
        'product':product,
        'comments':comments
    }
    return render(request, 'home/discussion.html', context)

def comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        print comment
        product_id = request.POST['product_id']
        print product_id
        user_id = request.session['id']
        print user_id
        Comment.objects.AddComment(comment, product_id, user_id)
    return redirect(reverse('home:discussion', kwargs={'id':product_id}))
