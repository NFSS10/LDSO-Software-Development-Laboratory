from django.conf.urls import include, url
from . import views

app_name = "products"

urlpatterns = [
    url(r'^register_product', views.register_product, name="register_product"),
    url(r'^show-product(?P<product_id>[0-9]+)/$', views.show_product, name="show-product"),
    url(r'^add-product', views.add_product, name="add-product"),
    url(r'^list_products/', views.list_products, name='list_products'),
    url(r'^manage_products/', views.manage_products, name='manage_products'),
    url(r'^deactivateProduct(?P<product_id>[0-9]+)/$', views.deactivateProduct, name='deactivateProduct'),
    url(r'^activateProduct(?P<product_id>[0-9]+)/$', views.activateProduct, name='activateProduct')
]
