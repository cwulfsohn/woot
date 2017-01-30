from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^dummy/$', views.dummy, name="dummy"),
    url(r'^product/show/(?P<id>\d+)$', views.show_product, name="show_product"),
    url(r'^product/new/$', views.new_product, name="new_product"),
    url(r'^product/new/add/$', views.add_product, name="add_product"),
    url(r'^product/new/image/(?P<id>\d+)$', views.new_image, name="new_image"),
    url(r'^product/new/image/(?P<id>\d+)/upload$', views.upload_image, name="upload_image"),
]
