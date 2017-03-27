from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^profile__edit/$', views.profile__edit, name='profile__edit'),
    url(r'^store/(?P<id>[0-9]+)/$', views.market_detail, name='market_detail'),
    url(r'^get_market_sales/$', views.get_market_sales, name='get_market_sales'),
    url(r'^get_market_saless/$', views.get_market_saless, name='get_market_saless'),
    url(r'^check_login/$', views.check_login, name='check_login'),
    url(r'^profile/$', views.profile, name='profile'),


]

