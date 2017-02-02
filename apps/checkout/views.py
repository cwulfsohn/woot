from django.shortcuts import render, redirect, reverse
from ..home.models import Product, Cart
from ..login.models import User
from django.db.models import Count
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime

# <QuerySet [{'product__name__count': 2, 'product__name': u'Beneful Original'}, {'product__name__count': 1, 'product__name': u'Nurf Hoop!'}]>

def index(request):
    if "id" not in request.session:
        return redirect(reverse('login:index'))
    user = User.objects.get(id=request.session["id"])
    products = Product.objects.filter(products_cart__user=user).filter(products_cart__active=True).filter(active=True).distinct()
    quantities = Cart.objects.filter(user=user).filter(active=True).filter(product__active=True).values('product__name').order_by().annotate(Count('product__name'))
    cart_products = []
    total = 0
    for product in products:
        cart_product= {"id":product.id, "name":product.name, "primary_image":product.primary_image}
        for quantity in quantities:
            if quantity["product__name"] == product.name:
                cart_product["quantity"] = quantity["product__name__count"]
        cart_product["price"] = cart_product["quantity"] * product.price
        cart_products.append(cart_product)
        total += cart_product["price"]
    context = {"cart_products":cart_products, "total":total}
    return render(request, 'checkout/index.html', context)

def add_cart(request, id):
    pass
    if request.method == "POST":
        quantity = int(request.POST["quantity"])
        user = User.objects.get(id=request.session["id"])
        product = Product.objects.get(id=id)
        for i in range(quantity):
            Cart.objects.create(product=product, user=user)
    return redirect(reverse('home:show_product', kwargs={'id':id}))

def remove(request, id):
    user = User.objects.get(id=request.session["id"])
    Cart.objects.filter(user=user).filter(product__id=id).delete()
    return redirect(reverse('checkout:index'))

def buy(request):
    if "id" not in request.session:
        return redirect(reverse('login:index'))
    user = User.objects.get(id=request.session["id"])
    products = Product.objects.filter(products_cart__user=user).filter(products_cart__active=True).filter(active=True).distinct()
    quantities = Cart.objects.filter(user=user).filter(active=True).filter(product__active=True).values('product__name').order_by().annotate(Count('product__name'))
    cart_products = []
    total = 0
    for product in products:
        cart_product= {"id":product.id, "name":product.name, "primary_image":product.primary_image}
        for quantity in quantities:
            if quantity["product__name"] == product.name:
                cart_product["quantity"] = quantity["product__name__count"]
        cart_product["price"] = cart_product["quantity"] * product.price
        cart_products.append(cart_product)
        total += cart_product["price"]
    print request.session['card_id']
    try:
        address = Address.objects.get(id=request.session["address_id"])
    except:
        address = False
    try:
        card = CreditCard.objects.get(id=request.session["card_id"])
    except:
        card = False
    context = {"cart_products":cart_products,
                "total":total,
                "address":address,
                "card":card,
            }
    return render(request, 'checkout/buy.html', context)

def address(request):
    user = User.objects.get(id=request.session["id"])
    addresses = Address.objects.filter(user=user)
    context = {"addresses":addresses}
    return render(request, 'checkout/address.html', context)

def add_address(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session["id"])
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        if 'unit' in request.POST:
            unit = request.POST['unit']
        else:
            unit=None
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        country = request.POST['country']
        Address.objects.create(user=user, first_name=first_name, last_name=last_name, address=address, unit=unit, city=city, state=state, zip_code=zipcode, country=country)
    return redirect(reverse('checkout:address'))

def select_address(request):
    if request.method=="POST":
        if "address_id" not in request.POST:
            messages.error(request, "You must select an address")
            return redirect(reverse('checkout:address'))
        request.session["address_id"] = request.POST["address_id"]
    return redirect(reverse('checkout:billing'))

def select_card(request):
    if request.method=="POST":
        if "card_id" not in request.POST:
            messages.error(request, "You must select an card")
            return redirect(reverse('checkout:billing'))
        request.session["card_id"] = request.POST["card_id"]
    return redirect(reverse('checkout:buy'))

def billing(request):
    user = User.objects.get(id=request.session["id"])
    cards = CreditCard.objects.filter(user=user)
    context = {"cards":cards}
    return render(request, 'checkout/billing.html', context)

def add_card(request):
    if request.method=="POST":
        user = User.objects.get(id=request.session["id"])
        full_name = request.POST["full_name"]
        last_four = request.POST["card_number"][-4:]
        card_number = bcrypt.hashpw(request.POST["card_number"].encode(), bcrypt.gensalt())
        request.POST["card_number"]
        expiration_date = datetime.strptime(request.POST["expiration_date"], "%m/%y").date()
        cvv = bcrypt.hashpw(request.POST["cvv"].encode(), bcrypt.gensalt())
        if request.POST["billing_address"] == "True" and "address_id" in request.session:
            address = Address.objects.get(id=request.session["address_id"])
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            if 'unit' in request.POST:
                unit = request.POST['unit']
            else:
                unit=None
            city = request.POST['city']
            state = request.POST['state']
            zipcode = request.POST['zipcode']
            country = request.POST['country']
            address = Address.objects.create(user=user, first_name=first_name, last_name=last_name, address=address, unit=unit, city=city, state=state, zip_code=zipcode, country=country)
        card = CreditCard.objects.create(last_four=last_four, user=user, address=address, full_name=full_name, card_number=card_number, cvv=cvv, expiration_date=expiration_date)
    return redirect(reverse('checkout:billing'))
