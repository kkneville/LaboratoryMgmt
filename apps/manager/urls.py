from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="showusers"),
    url(r'^index$', views.index, name="showusers"),
    url(r'^(?P<id>\d+)/profile$', views.showuser, name="showuser"),
    url(r'^(?P<id>\d+)/edit$', views.edituser, name="edituser"),
    url(r'^(?P<id>\d+)/delete$', views.deletecheck, name="deletecheck"),

]
