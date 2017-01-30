from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^dummy/$', views.dummy, name="dummy"),
    url(r'^product/add/$', views.add_product, name="add_product")
]
