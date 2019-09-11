from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^home', views.index, name='home'),
    url(r'^utilizadores/', include('WebSite.utilizadores.urls')),
    url(r'^administrador/', include('WebSite.administrador.urls')),
	url(r'^ferramentas/', include('WebSite.tools.urls')),
    url(r'^eventos/', include('WebSite.events.urls')),
    url(r'^blog/', include('WebSite.blog.urls')),
    url(r'^store/', include('WebSite.store.urls', namespace="store")),
    url(r'^products/', include('WebSite.products.urls', namespace="products")),
    url(r'^cart/', include('WebSite.cart.urls', namespace="cart")),
    url(r'^purchase/', include('WebSite.purchase.urls', namespace="purchase")),
    url(r'^sobre/', views.sobre, name='sobre'),
    url(r'^contacto/', views.contactMe, name='contacto')


]
