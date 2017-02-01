from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^add_cart/(?P<id>\d+)$', views.add_cart, name="add_cart"),
]
