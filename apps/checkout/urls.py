from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^buy/$', views.buy, name="buy"),
    url(r'^address/$', views.address, name="address"),
    url(r'^billing/$', views.billing, name="billing"),
    url(r'^purchase/$', views.purchase, name="purchase"),
    url(r'^success/$', views.success, name="success"),
    url(r'^billing/add/$', views.add_card, name="add_card"),
    url(r'^address/add$', views.add_address, name="add_address"),
    url(r'^address/select$', views.select_address, name="select_address"),
    url(r'^billing/select$', views.select_card, name="select_card"),
    url(r'^add_cart/(?P<id>\d+)$', views.add_cart, name="add_cart"),
    url(r'^remove/(?P<id>\d+)$', views.remove, name="remove"),


]
