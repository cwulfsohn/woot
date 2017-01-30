from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^product$', views.discussion, name="discussion")
]
