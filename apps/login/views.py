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
            request.session["admin_level"] = user["user"].admin_level
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
            if "id" not in request.session:
                request.session["admin_level"] = user["user"].admin_level
                request.session['name'] = user["user"].first_name
                request.session["username"] = user["user"].username
                request.session["id"] = user["user"].id
            return redirect('home:index')
    else:
        return redirect(reverse('login:index'))

def logout(request):
    request.session.clear()
    return redirect(reverse('login:index'))

def dashboard(request):
    print request.session["admin_level"]
    if request.session["admin_level"] != 4:
        return redirect(reverse('home:index'))
    users = User.objects.all()
    context = {
            "users":users,
    }
    return render(request, 'login/dashboard_admin.html', context)

def new(request):
    return render(request, 'login/new.html')

def edit_admin(request, id):
    try:
        user = User.objects.get(id=id)
        context = {"user":user}
    except:
        redirect(reverse('login:dashboard'))
    return render(request, 'login/edit_admin.html', context)

def update(request, id):
    if request.POST["edit_field"] == "information":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        if "admin_level" in request.POST:
            admin_level= request.POST["admin_level"]
            user = User.objects.update_name(username, email, first_name, last_name, id, admin_level)
        else:
            user = User.objects.update_name(username, email, first_name, last_name, id)
    elif request.POST["edit_field"] == "password":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user = User.objects.update_password(password, confirm_password, id)
    if "errors" in user:
        for error in user["errors"]:
            messages.error(request, error)
            if request.session["admin_level"] == 4:
                return redirect(reverse("login:edit_admin", kwargs={'id':id}))
            return redirect(reverse('login:edit'))
    if request.session["id"] == user["user"].id:
        request.session["admin_level"] = user["user"].admin_level
        request.session['name'] = user["user"].first_name
        request.session["username"] = user["user"].username
    return redirect(reverse("login:dashboard"))

def delete_user(request, id):
    if request.session["id"] == id:
        messages.error(request, "Can't delete yourself")
    else:
        User.objects.get(id=id).delete()
    return redirect(reverse('login:dashboard'))

def edit(request):
    try:
        user = User.objects.get(id=request.session['id'])
    except:
        redirect(reverse('home:index'))
    context = {
            "user":user
    }
    return render(request, 'login/edit.html', context)
