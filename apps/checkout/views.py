from django.shortcuts import render, redirect, reverse
from ..home.models import Product

def index(request):
    return render(request, 'checkout/index.html')

def add_cart(request, id):
    pass
    # if request.method == "POST":
    #     quantity = request.POST['quantity']
    #     quantity = int(quantity)
    #     if not "cart" in request.session or not request.session['cart']:
    #         request.session["cart"] = [id]
    #     cart = request.session["cart"]
    #     # for quantity in range(quantity):
    #     cart = cart.append(id)
    #     for die in request.session["cart"]:
    #         print die
    #     request.session["cart"] = cart
    # return redirect(reverse('home:show_product', kwargs={'id':id}))
