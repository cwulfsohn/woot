from django.shortcuts import render, redirect, reverse

def index(request):
    return render(request, 'checkout/index.html')

def add_cart(request):
    if request.method == "POST":
        pass
    return redirect(reverse('home:show'))
