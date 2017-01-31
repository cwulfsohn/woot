from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import User


def index(request):
    return render(request, 'login/index.html')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.login(email, password)
        if "errors" in user:
            for error in user["errors"]:
                messages.error(request, error)
            return redirect('login:index')
        else:
            request.session['name'] = user["user"].first_name
            request.session["username"] = user["user"].username
            request.session["id"] = user["user"].id
            return redirect('home:index')
    else:
        return redirect(reverse('login:index'))

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user = User.objects.add_user(username, first_name, last_name, email, password, confirm_password)
        if "errors" in user:
            for error in user["errors"]:
                messages.error(request, error)
            return redirect(reverse('login:index'))
        else:
            request.session['name'] = user["user"].first_name
            request.session["username"] = user["user"].username
            request.session["id"] = user["user"].id
            return redirect('home:index')
    else:
        return redirect(reverse('login:index'))

def logout(request):
    request.session.clear()
    return redirect(reverse('login:index'))
