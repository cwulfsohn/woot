from django.shortcuts import render, redirect, reverse, HttpResponse
from .models import *
from .forms import ImageUploadForm
from datetime import datetime, timedelta, date, time
from django.contrib import messages
from django.db.models import Count
from django.db.models import Avg
import json
import calendar
import decimal


def get_cart_products(request):
    user = User.objects.get(id=request.session["id"])
    products = Product.objects.filter(products_cart__user=user).filter(products_cart__active=True).filter(active=True).distinct()
    quantities = Cart.objects.filter(user=user).filter(active=True).filter(product__active=True).values('product__name').order_by().annotate(Count('product__name'))
    cart_products = []
    for product in products:
        cart_product= {"id":product.id, "name":product.name, "primary_image":product.primary_image}
        for quantity in quantities:
            if quantity["product__name"] == product.name:
                cart_product["quantity"] = quantity["product__name__count"]
        if product.quantity < cart_product["quantity"]:
            cart_product["quantity"] = product.quantity
        cart_product["price"] = cart_product["quantity"] * product.price
        cart_products.append(cart_product)
    return cart_products


# Create your views here.
def index(request):
    if 'id' not in request.session:
        request.session.clear()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    today = datetime.now().date()
    try:
        daily_deal = Product.objects.get(daily_deal=True, deal_date = today)
        daily_deal.active = True
        daily_deal.save()
    except:
        daily_deal = Product.objects.filter(daily_deal=True, active = True, quantity__gt=0).order_by('expire_date')[:1]
        daily_deal = daily_deal[0]
    deal_images = Image.objects.filter(product = daily_deal)
    comments = Comment.objects.filter(product = daily_deal).order_by('-created_at')[:2]
    percent_off = Product.objects.percent_off(daily_deal.price, daily_deal.list_price)
    bestsellers = Product.objects.annotate(sold=Count('product_purchase__product_id')).exclude(id = daily_deal.id).order_by('-sold')[:4]
    new_items = Product.objects.exclude(id= daily_deal.id).order_by('-created_at')[:4]
    last_chance = Product.objects.exclude(id = daily_deal.id).filter(quantity__gt=0).order_by('quantity')[:4]
    today = datetime.now().date()
    start_date = datetime.min.time()
    end_date = datetime.max.time()
    start_range = datetime.combine(today, start_date)
    end_range = datetime.combine(today, end_date)
    the_daily_deal = []
    deal = Product.objects.filter(daily_deal = 1).filter(deal_date__range=[str(start_range),str(end_range)])
    time_count = 1
    for deals in deal:
        while time_count < 25:
            counter = 0
            holder = []
            for purchases in Purchase.objects.filter(product_id = deals.id):
                if purchases.created_at.strftime("%H") == str(time_count):
                    counter += 1
            holder.append(time_count)
            holder.append(counter)
            the_daily_deal.append(holder)
            time_count += 1
    context = {'categories': categories,
               'subcategories': subcategories,
               'daily_deal': daily_deal,
               'deal_image': deal_images,
               'percent_off': percent_off,
               'comments': comments,
               'today': today,
               'bestsellers': bestsellers,
               'new_items': new_items,
               'last_chance': last_chance,
               'the_daily_deal':json.dumps(the_daily_deal)
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
            product.primary_image = form.cleaned_data['image']
            product.save()
            relative_path = product.primary_image.name[17:]
            Product.objects.filter(id=id).update(primary_image=relative_path)
            return redirect(reverse('home:features', kwargs={'id':id}))
    return redirect(reverse('home:new_image', kwargs={'id':id}))

def category(request, id):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    category = Category.objects.get(id = id)
    this_cat_subcategories = Subcategory.objects.filter(category = category)
    ending_soon = Product.objects.filter(subcategory__category=category, active = True, quantity__gt=0).order_by('expire_date')[:4]
    total_products = {}
    category_total = 0
    for cat in this_cat_subcategories:
        total_products[cat.id]= Product.objects.filter(subcategory = cat, active = True, quantity__gt = 0).count()
        category_total += total_products[cat.id]
    if ending_soon:
        main_product = ending_soon[0]
        images = Image.objects.filter(product=main_product)
        comments = Comment.objects.filter(product = main_product).order_by('-created_at')[:1]
        percent_off = Product.objects.percent_off(main_product.price, main_product.list_price)
        all_products = Product.objects.filter(subcategory__category=category, active = True, quantity__gt=0).exclude(id = main_product.id).order_by('expire_date')
    else:
        all_products = Product.objects.filter(subcategory__category=category).filter(active=True).order_by('expire_date')
        main_product = False
        images = False
        comments = False
        percent_off = False
    context = {'categories': categories,
               'subcategories': subcategories,
               'this_category': category,
               'this_cat_subcategories': this_cat_subcategories,
               'main_product': main_product,
               'images': images,
               'comments': comments,
               'percent_off': percent_off,
               'all_products': all_products,
               'total_products': total_products,
               'category_total': category_total,
               }
    return render(request, 'home/category.html', context)

def subcategory(request, id):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    subcategory = Subcategory.objects.get(id = id)
    category = Category.objects.get(id = subcategory.category_id)
    this_cat_subcategories = Subcategory.objects.filter(category = category)
    total_products = {}
    category_total = 0
    for cat in this_cat_subcategories:
        total_products[cat.id]= Product.objects.filter(subcategory = cat, active = True, quantity__gt = 0).count()
        category_total += total_products[cat.id]
    all_products = Product.objects.filter(subcategory = subcategory, active = True, quantity__gt=0).order_by('expire_date')
    context = {'categories': categories,
               'subcategories': subcategories,
               'category': category,
               'subcategory': subcategory,
               'this_cat_subcategories': this_cat_subcategories,
               'all_products': all_products,
               'total_products': total_products,
               'category_total': category_total,
               }
    return render(request, 'home/subcategory.html', context)

def show_product(request, id):
    try:
        cart_products = get_cart_products(request)
    except KeyError:
        cart_products = False
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    product = Product.objects.get(id=id)
    if product.active == False:
        active = False
    else:
        active = True
    over = False
    if cart_products:
        for cart_product in cart_products:
            if cart_product["id"] == int(id):
                if cart_product["quantity"] >= product.quantity:
                    over = True
    images = Image.objects.filter(product=product)
    comments = Comment.objects.filter(product = product).order_by('-created_at')[:2]
    percent_off = Product.objects.percent_off(product.price, product.list_price)
    features = Feature.objects.filter(product=product)
    specifications = Specifications.objects.filter(product=product)
    try:
        Rating.objects.get(product_id = product.id, user_id = request.session['id'])
        rated = True
    except:
        rated = False
    try:
        avg_rating = product.product_rating.aggregate(Avg('rating')).values()[0]
        avg_rating = round(avg_rating, 1)
    except:
        pass
    today = datetime.now().date()
    first_day = datetime.now().date()-timedelta(days=6)
    daily_deal = []
    product_id = Product.objects.get(id = id)
    category_id = Category.objects.get(subcategories__products__id = product_id.id)
    product_list = Product.objects.filter(subcategory__category__category = category_id.category)
    category_count = 0
    product_percent = []
    for category_products in product_list:
        for purchases in Purchase.objects.filter(product_id = category_products.id):
            category_count += 1
    for category_products in product_list:
        count = 0
        for purchases in Purchase.objects.filter(product_id = category_products.id):
            count += 1
        holder = []
        holder.append(category_products.name)
        holder.append(float(float(count)/float(category_count)))
        product_percent.append(holder)
    show_item = 0
    for purchases in Purchase.objects.filter(product_id = product_id.id):
        show_item += 1
    purchase_deal  = []
    purchase_deal.append(product_id.name)
    purchase_deal.append(show_item)
    daily_deal.append(purchase_deal)
    product_object = Product.objects.filter(daily_deal = 1)
    for products in product_object:
        deal = []
        purchase_count = 0
        if str(products.deal_date) <= str(today) and str(products.deal_date) > str(first_day):
            for purchases in Purchase.objects.filter(product_id = products.id):
                purchase_count += 1
            deal.append(products.name)
            deal.append(purchase_count)
            daily_deal.append(deal)
    print daily_deal
    context = {'categories': categories,
               'subcategories': subcategories,
               'product': product,
               'images': images,
               'comments': comments,
               'percent_off': percent_off,
               'rated': rated,
               'avg_rating': avg_rating,
               'features': features,
               'specifications': specifications,
               'over':over,
               'active': active,
               'daily_deal':json.dumps(daily_deal),
               'product_percent':json.dumps(product_percent)
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
        if len(feature_header) < 2:
            messages.error(request, "Feature Header does not fit criteria length")
        elif len(feature_description) < 2:
            messages.error(request, "Feature Description does not fit criteria length")
        else:
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
        check_category = request.POST['specification_header']
        if len(description) < 2:
            messages.error(request, "Description deos not fit critera")
            return redirect(reverse('home:specifications', kwargs={'id':id}))
        try:
            if SpecificationCategories.objects.get(category = check_category):
                messages.error(request, "Category is already created")
                return redirect(reverse('home:specifications', kwargs={'id':id}))
        except:
            try:
                checked =  request.POST['add_spec_header']
                if checked:
                    category = request.POST['specification_header']
                    SpecificationCategories.objects.create(category = category)
                    category_id = SpecificationCategories.objects.get(category = category)
                    product = Product.objects.get(id = id)
                    Specifications.objects.create(product = product, spec_category=category_id, value=description)
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
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    try:
        user = User.objects.get(id = request.session["id"])
    except:
        user = False
    product = Product.objects.get(id = id)
    comments = Comment.objects.filter(product=id).order_by("-created_at")
    category = Category.objects.filter(subcategories__products__id = id)
    main_category = Category.objects.get(subcategories__products__id = id)
    context = {
        'categories': categories,
        'subcategories': subcategories,
        'user':user,
        'product':product,
        'comments':comments,
        'category':category,
        'main_category':main_category,
    }
    return render(request, 'home/discussion.html', context)

def comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        product_id = request.POST['product_id']
        if len(comment) < 2:
            messages.error(request, "Description does not meet length criteria")
            return redirect(reverse('home:discussion', kwargs={'id':product_id}))
        user_id = request.session['id']
        Comment.objects.AddComment(comment, product_id, user_id)
    return redirect(reverse('home:discussion', kwargs={'id':product_id}))

def reply(request, id):
    if request.method == 'POST':
        comment_id = id
        reply = request.POST['comment']
        product_id = request.POST['product_id']
        if len(reply) < 2:
            messages.error(request, "Description does not meet length criteria")
            return redirect(reverse('home:discussion', kwargs={'id':product_id}))
        user_id = request.session['id']
        Replies.objects.AddReply(reply, product_id, user_id, comment_id)
    return redirect(reverse('home:discussion', kwargs={'id':product_id}))

def delete_comment(request, id, product_id):
    delete_comment = Comment.objects.get(id=id)
    delete_comment.delete()
    return redirect(reverse('home:discussion', kwargs={'id':product_id}))

def delete_replies(request, id, product_id):
    delete_reply = Replies.objects.get(id=id)
    delete_reply.delete()
    return redirect(reverse('home:discussion', kwargs={'id':product_id}))

def rating(request, id):
    if request.method == 'POST':
        user = User.objects.get(id = request.session['id'])
        product = Product.objects.get(id = id)
        rating = request.POST['rating']
        Rating.objects.create(rating = rating, user = user, product = product)
        avg_rating = Rating.objects.filter(product__id = id)
        count = 0
        avg_rate = 0
        for ratings in avg_rating:
            count += 1
            avg_rate += ratings.rating
        product_rating = round(float(avg_rate)/float(count),2)
        Product.objects.filter(id=id).update(rating = product_rating)
    return redirect(reverse('home:show_product', kwargs={'id':id}))

def daily_stat(request, id):
    today = datetime.now().date()
    start_date = datetime.min.time()
    end_date = datetime.max.time()
    start_range = datetime.combine(today, start_date)
    end_range = datetime.combine(today, end_date)
    the_daily_deal = []
    deal = Product.objects.filter(daily_deal = 1).filter(deal_date__range=[str(start_range),str(end_range)])
    time_count = 1
    for deals in deal:
        while time_count < 25:
            counter = 0
            holder = []
            for purchases in Purchase.objects.filter(product_id = deals.id):
                if purchases.created_at.strftime("%H") == str(time_count):
                    counter += 1
            holder.append(time_count)
            holder.append(counter)
            the_daily_deal.append(holder)
            time_count += 1
    context = {
        'the_daily_deal':json.dumps(the_daily_deal)
    }
    return render(request, 'home/daily_stat.html', context)

def manage_products(request):
    if 'admin_level' not in request.session:
        return redirect('home:index')
    all_products = Product.objects.all()
    description_teasers = {}
    for product in all_products:
        if len(product.description) > 50:
            description_teasers[product.id] = product.description[0:50] + "..."
        else:
            description_teasers[product.id] = product.description
    context = {'all_products': all_products,
               'description_teasers': description_teasers}
    return render(request, 'home/product_dashboard.html', context)

def edit_product(request, id):
    if 'admin_level' not in request.session:
        return redirect('home:index')
    product = Product.objects.get(id = id)
    current_subcategory = Subcategory.objects.get(id = product.subcategory.id)
    current_category = Category.objects.get(id = current_subcategory.category.id)
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    product.expire_date = datetime.strftime(product.expire_date, "%m/%d/%Y")
    if product.deal_date:
        product.deal_date = datetime.strftime(product.deal_date, "%m/%d/%Y")
    context = {'product': product,
               'current_subcategory': current_subcategory,
               'current_category': current_category,
               'categories': categories,
               'subcategories': subcategories,
               }
    return render(request, 'home/edit_product.html', context)

def update_product(request, id):
    if 'admin_level' not in request.session:
        return redirect('home:index')
    if request.method == "POST":

        name = request.POST["name"]
        description = request.POST["description"]
        category = request.POST["category"]
        sub = str(category) + "_subcategory"
        subcategory = Subcategory.objects.get(id=request.POST[sub])
        price = request.POST["price"]
        list_price = request.POST["list_price"]
        active = request.POST["active"]
        daily_deal = request.POST["daily_deal"]
        if request.POST["deal_date"]:
            deal_date=request.POST["deal_date"]
        else:
            deal_date=None
        quantity = request.POST["quantity"]
        expire_date = request.POST["expire_date"]
        primary_image = request.POST["primary_image"]
        errors = Product.objects.validate(name,description,price,list_price,quantity,expire_date, deal_date, id)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(reverse('home:edit_product', kwargs={'id':id}))
        expire_date = datetime.strptime(expire_date, "%m/%d/%Y")
        if deal_date:
            deal_date = datetime.strptime(deal_date, "%m/%d/%Y")
            Product.objects.filter(id=id).update(name=name, description=description, subcategory=subcategory, price=price, list_price=list_price, active=active, daily_deal=daily_deal, quantity=quantity, expire_date=expire_date, deal_date=deal_date, primary_image=primary_image)
        else:
            Product.objects.filter(id=id).update(name=name, description=description, subcategory=subcategory, price=price, list_price=list_price, active=active, daily_deal=daily_deal, quantity=quantity, expire_date=expire_date, primary_image=primary_image)
        message = "Product Successfully Updated!"
        messages.success(request, message)
        return redirect('home:manage_products')

def delete_product(request, id):
    Product.objects.filter(id=id).delete()
    message = "Product Successfully Deleted!"
    messages.success(request, message)
    return redirect('home:manage_products')

def orders(request):
    if not "id" in request.session:
        return redirect(reverse('home:index'))
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    user = request.session["id"]
    orders = Order.objects.filter(user=user).order_by("-created_at")
    order_totals = {}
    for order in orders:
        total = 0
        purchases = Purchase.objects.filter(order=order)
        for purchase in purchases:
            total += purchase.product.price
        order_totals[order.id] = total
    context = {"orders":orders, "categories":categories, "subcategories":subcategories, "order_totals":order_totals}
    return render(request, 'home/orders.html', context)

def get_order_basket(request, id):
    user = User.objects.get(id=request.session["id"])
    order = Order.objects.get(id=id)
    order_basket = []
    products = Product.objects.filter(product_purchase__order=order).distinct()
    quantities = Order.objects.filter(id=order.id).values('order_purchases__product__name').order_by().annotate(Count('order_purchases__product__name'))
    for product in products:
        order_product= {"id":product.id, "name":product.name, "primary_image":product.primary_image}
        for quantity in quantities:
            if quantity["order_purchases__product__name"] == product.name:
                order_product["quantity"] = quantity["order_purchases__product__name__count"]
        order_product["price"] = order_product["quantity"] * product.price
        order_basket.append(order_product)
    return order_basket

def order(request, id):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    user = User.objects.get(id=request.session["id"])
    order = Order.objects.get(id=id)
    if not order.user == user:
        return redirect(reverse('home:index'))
    order_basket = get_order_basket(request, id)
    total = 0
    for product in order_basket:
        total =+ product["price"]
    context = {"order":order, "order_basket":order_basket, "total":total, "categories": categories, "subcategories": subcategories}
    return render(request, 'home/order.html', context)

def daily_deals(request):
    if not request.session["admin_level"] == 4:
        return redirect(reverse('home:index'))
    days = []
    for i in range(30):
        new_date = date.today() + timedelta(i)
        days.append(new_date)
    deals = Product.objects.filter(daily_deal=True)
    deal_days = []
    for deal in deals:
        deal.deal_date = deal.deal_date.date()
        print deal.deal_date
    for day in days:
        deal_day = {'day':day}
        for deal in deals:
            if deal.deal_date == day:
                deal_day["deal"] = deal
                print deal.name
        deal_days.append(deal_day)
    context = {"deal_days":deal_days, "days":days, "deals":deals}
    return render(request, 'home/daily_deals.html', context)

def remove_deal(request, id):
    if not request.method == "POST":
        return redirect(reverse('home:index'))
    Product.objects.filter(id=id).update(daily_deal=False)
    return redirect(reverse('home:daily_deals'))

def change_deal(request, id):
    if not request.method == "POST":
        return redirect(reverse('home:index'))
    product = Product.objects.get(id=id)
    deal_date = datetime.strptime(request.POST["deal_date"], "%b. %d, %Y")
    print deal_date
    switch_product = Product.objects.filter(deal_date=deal_date)
    if switch_product:
        Product.objects.filter(deal_date=deal_date).update(deal_date=product.deal_date)

    product.deal_date = deal_date
    product.save()
    return redirect(reverse('home:daily_deals'))
