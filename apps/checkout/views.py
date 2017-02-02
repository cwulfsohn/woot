from django.shortcuts import render, redirect, reverse
from ..home.models import Product, Cart, Purchase, Order, Subcategory
from ..login.models import User
from django.db.models import Count
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime

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
        cart_product["price"] = cart_product["quantity"] * product.price
        cart_products.append(cart_product)
    return cart_products

def get_total(cart_products):
    total = 0
    for cart_product in cart_products:
        total += cart_product["price"]
    return total

def index(request):
    if "id" not in request.session:
        return redirect(reverse('login:index'))
    cart_products = get_cart_products(request)
    total = get_total(cart_products)
    user = User.objects.get(id=request.session["id"])
    expireds = Product.objects.filter(products_cart__user=user).filter(products_cart__active=True).filter(active=False).distinct()
    context = {"cart_products":cart_products, "total":total, "expireds":expireds}
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
    cart_products = get_cart_products(request)
    total = get_total(cart_products)
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
        zip_code = request.POST['zipcode']
        country = request.POST['country']
        errors = Address.objects.address_validator(first_name, last_name, address, city, state, zip_code, country)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            Address.objects.create(user=user, first_name=first_name, last_name=last_name, address=address, unit=unit, city=city, state=state, zip_code=zip_code, country=country)
    return redirect(reverse('checkout:address'))

def select_address(request):
    if request.method=="POST":
        if "address_id" not in request.POST:
            messages.error(request, "You must select an address")
            return redirect(reverse('checkout:address'))
        request.session["address_id"] = request.POST["address_id"]
        if "card_id" in request.session:
            return redirect(reverse("checkout:buy"))
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
        card_number = request.POST["card_number"]
        expiration_date = request.POST["expiration_date"]
        cvv = request.POST["cvv"]
        errors = []
        errors = CreditCard.objects.card_validator(full_name, card_number, expiration_date, cvv)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(reverse('checkout:billing'))
        card_number = bcrypt.hashpw(card_number.encode(), bcrypt.gensalt())
        cvv = bcrypt.hashpw(cvv.encode(), bcrypt.gensalt())
        expiration_date = datetime.strptime(expiration_date, "%m/%y").date()
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
            errors = Address.objects.address_validator(first_name, last_name, address, city, state, zipcode, country)
            if errors:
                for error in errors:
                    messages.error(request, error)
                    return redirect(reverse('checkout:billing'))
            else:
                address = Address.objects.create(user=user, first_name=first_name, last_name=last_name, address=address, unit=unit, city=city, state=state, zip_code=zipcode, country=country)
        card = CreditCard.objects.create(last_four=last_four, user=user, address=address, full_name=full_name, card_number=card_number, cvv=cvv, expiration_date=expiration_date)
    return redirect(reverse('checkout:billing'))

def purchase(request):
    if not request.method == "POST":
        return redirect(reverse('checkout:buy'))
    user = User.objects.get(id=request.session["id"])
    address = Address.objects.get(id=request.session["address_id"])
    address_message = "Shipped to: " + address.address
    card = CreditCard.objects.get(id=request.session["card_id"])
    card_message = "Payment: card ending in ***" + card.last_four
    messages.add_message(request, messages.INFO, address_message)
    messages.add_message(request, messages.INFO, card_message)
    del request.session["address_id"]
    del request.session["card_id"]
    cart_products = get_cart_products(request)
    total = get_total(cart_products)
    user = User.objects.get(id=request.session["id"])
    order = Order.objects.create(user=user)
    for cart_product in cart_products:
        product = Product.objects.get(id=cart_product['id'])
        for quantity in range(cart_product['quantity']):
            Purchase.objects.create(user=user, product=product, order=order)
            product.quantity = product.quantity - 1
            if product.quantity <= 0:
                product.active = False
            product.save()
        Cart.objects.filter(user=user, product=product).update(active=False)
    return redirect(reverse('checkout:success'))

def success(request):
    user = User.objects.get(id=request.session["id"])
    order = Order.objects.filter(user=user).order_by('-id')[0]
    products = Product.objects.filter(product_purchase__order=order)
    saved = 0
    total = 0
    other_products = Product.objects.filter(subcategory=products[0].subcategory).exclude(id=products[0].id)[:6]
    for product in products:
        saved += product.list_price - product.price
        total += product.price
    context = {"order":order, "products":products, "saved":saved, "other_products":other_products, "total":total}
    return render(request, 'checkout/success.html', context)
