from django.shortcuts import render, redirect, reverse
from ..home.models import Product, Cart
from ..login.models import User

def index(request):
    user = User.objects.get(id=request.session["id"])
    products = Product.objects.filter(products_cart__user=user).filter(products_cart__active=True)
    context = {"products":products}
    return render(request, 'checkout/index.html', context)

def add_cart(request, id):
    pass
    if request.method == "POST":
        quantity = int(request.POST["quantity"])
        user = User.objects.get(id=request.session["id"])
        product = Product.objects.get(id=id)
        Cart.objects.create(product=product, user=user)
    return redirect(reverse('home:show_product', kwargs={'id':id}))
