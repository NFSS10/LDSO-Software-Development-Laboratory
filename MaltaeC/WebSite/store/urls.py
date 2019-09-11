from django.conf.urls import url, include
from . import views

app_name = "products"


urlpatterns = [
    #url(r'^$',views.index),
    url(r'^list_products/', views.list_products, name='list_products'),
    url(r'^search_products/', views.search_products, name='search_products'),
]
