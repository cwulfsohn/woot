from django.shortcuts import render, redirect, reverse
from .models import *
from ..login.models import *
from ..home.models import *


def discussion(request, id):
    print request.session['id']
    user = User.objects.get(id = request.session["id"])
    product = Product.objects.get(id = id)
    comments = Comment.objects.filter(product=id).order_by("created_at")
    context = {
        'user':user,
        'product':product,
        'comments':comments
    }
    return render(request, 'discussions/index.html', context)

def comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        print comment
        product_id = request.POST['product_id']
        print product_id
        user_id = request.session['id']
        print user_id
        Comment.objects.AddComment(comment, product_id, user_id)
    return redirect(reverse('discussions:discussion', kwargs={'id':product_id}))
