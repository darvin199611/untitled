from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^profile__edit/$', views.profile__edit, name='profile__edit'),
    url(r'^store/(?P<id>[0-9]+)/$', views.market_detail, name='market_detail'),
]

