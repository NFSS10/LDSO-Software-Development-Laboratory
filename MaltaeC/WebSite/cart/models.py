from django.db import models
from django.conf import settings
from WebSite.utilizadores.models import BaseUser
from WebSite.products.models import Product


class Cart(models.Model):
    user = models.ForeignKey('utilizadores.BaseUser', on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey('Cart')
    product = models.ForeignKey('products.Product',on_delete=models.CASCADE)
    quantidade = models.IntegerField()

