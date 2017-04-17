from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^control/$', views.control, name='сontrol'),
    url(r'^store/(?P<id>[0-9]+)/control$', views.store_control, name='store_control'),
    url(r'^take_sales/$', views.take_sales, name='take_sales'),
    url(r'^delete_sale/$', views.delete_sale, name='delete_sale'),
]
