from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name="home"),
    url(r'^dashboard$', views.dashboard, name="dashboard"),
    url(r'^add$', views.add, name="add"),
    url(r'^logout$', views.logout, name="logout"),
]
