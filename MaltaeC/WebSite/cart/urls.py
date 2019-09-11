from django.conf.urls import include, url
from . import views

app_name = "cart"

urlpatterns = [
    url(r'^add_productCart', views.add_productCart, name='add_productCart'),
    url(r'^remove_fromCart(?P<cartItemid>[0-9]+)/$', views.remove_fromCart, name='remove_fromCart'),
    url(r'^show_cart', views.show_cart, name='show_cart')

]
