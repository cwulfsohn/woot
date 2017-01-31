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
    url(r'^product/new/features/(?P<id>\d+)$', views.features, name="features"),
    url(r'^product/new/add_features/(?P<id>\d+)$', views.add_feature, name="add_feature"),
    url(r'^product/new/delete_features/(?P<id>\d+)/(?P<feature_id>\d+)$', views.delete_feature, name="delete_feature"),
    url(r'^product/new/specifications/(?P<id>\d+)$', views.specifications, name="specifications"),
    url(r'^product/new/add_specification/(?P<id>\d+)$', views.add_specification, name="add_specification"),
    url(r'^product/new/delete_specification/(?P<id>\d+)/(?P<feature_id>\d+)$', views.delete_specification, name="delete_specification"),
]
