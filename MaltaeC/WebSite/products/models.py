from django.db import models
from django.conf import settings
from WebSite.utilizadores.models import BaseUser


class ProductType(models.Model):
    product_type = models.CharField(max_length=50)


"""Master Product model that contains universal product information
Product details unique to product types link into this model
"""


class MakerProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    maker = models.ForeignKey('utilizadores.BaseUser', on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=250, default='')
    # product_type = models.ForeignKey(ProductType, null=False)
    description = models.TextField(default='About this product', null=False, blank=False)
    short_desc = models.CharField(max_length=250, default='Shortened product description', null=False, blank=False)
    stock = models.IntegerField(default=0)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0.0, blank=True)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0.0, blank=True)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="image/", default='image/default.jpg')

    def decrement_stock(self, quantity):
        new_stock = self.stock - quantity
        if new_stock == 0:
            self.stock = 0
            self.active = False
            self.save()
        else:
            self.stock = new_stock
            self.save()


"""Central control for inventory checks to avoid inventory issues"""


class InventoryControl:

    def __init__(self, product):
        self.product = product

    """Disallows illegal product quantities when adding/updating shopping cart"""

    def clean_quantity(self, quantity):

        changed = False
        stock = self.product.stock
        limit_15 = 15

        if quantity > limit_15:
            quantity = limit_15
            changed = True
        if quantity > stock:
            quantity = stock
            changed = True
        if quantity <= 0:
            quantity = 1
            changed = True

        return quantity, changed

    def decrement_stock(self, quantity):
        self.product.decrement_stock(quantity)
