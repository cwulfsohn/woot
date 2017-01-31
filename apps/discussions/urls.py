from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^product/(?P<id>\d+)$', views.discussion, name="discussion"),
    url(r'^comment$', views.comment, name="comment"),
]
