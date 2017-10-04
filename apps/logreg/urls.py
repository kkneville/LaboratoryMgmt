from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="logregindex"),
    url(r'^index$', views.index, name="logregindex"),
    url(r'^login$', views.login, name="login"),
    url(r'^register$', views.register, name="register"),
    url(r'^adminadd$', views.adminadd, name="adminadd"),
    url(r'^adduser$', views.adduser, name="adduser"),
    url(r'^edit$', views.edit, name="edit"),
    url(r'^delete$', views.delete, name="delete"),
    url(r'^logout$', views.logout, name="logout"),
]
