from django.shortcuts import render, redirect, reverse
from .models import *
from ..login.models import *
from ..home.models import *

def discussion(request):
    print request.session['id']
    user = User.objects.get(id = request.session["id"])
    context = {
        'user':user
    }
    return render(request, 'discussions/index.html', context)

def dummy(request):

    return redirect(reverse('home:dummy'))
