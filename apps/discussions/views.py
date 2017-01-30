from django.shortcuts import render, redirect, reverse
from .models import *
from ..login.models import *
from ..home.models import *

def discussion(request):
    user = User.objects.get(id = request.session["id"])
    product = Product.objects.get(id = 1)
    comments = Comment.objects.filter(product=1)
    context = {
        'user':user,
        'product':product,
        'comments':comments
    }
    return render(request, 'discussions/index.html', context)

def comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        product_id = request.POST['product_id']
        user_id = request.session['id']
        Comment.objects.AddComment(comment, user_id, product_id)
    return redirect(reverse('discussions:discussion'))
