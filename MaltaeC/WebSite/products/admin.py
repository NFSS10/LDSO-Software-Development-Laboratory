from django.contrib import admin
from .models import Product,InventoryControl,MakerProduct,ProductType
# Register your models here.

admin.site.register(Product)
#admin.site.register(InventoryControl)
admin.site.register(MakerProduct)
admin.site.register(ProductType)
