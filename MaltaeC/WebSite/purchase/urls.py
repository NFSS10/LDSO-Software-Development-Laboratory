from django.conf.urls import include, url
from . import views

app_name = "purchase"

urlpatterns = [
    url(r'^checkout', views.checkout, name="checkout"),
    url(r'^show_purchase(?P<purchaseid>[0-9]+)/$', views.show_purchase, name='show_purchase'),
    url(r'^process(?P<purchaseid>[0-9]+)/$', views.process, name='process'),
    url(r'^cancel(?P<purchaseid>[0-9]+)/$', views.cancel, name='cancel'),
    url(r'^show_user_purchases', views.show_user_purchases, name="show_user_purchases"),
    url(r'^show_purchases_pending', views.show_purchases_pending, name="show_purchases_pending"),
    url(r'^paymentTransaction', views.paymentTransaction, name="paymentTransaction"),
    url(r'^show_All_purchases', views.show_All_purchases, name="show_All_purchases")


]
