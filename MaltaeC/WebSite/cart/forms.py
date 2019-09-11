from django import forms
from .models import CartItem


class CartForm(forms.Form):
    product = forms.CharField(max_length=300)
    quantidade = forms.IntegerField()
    # class Meta:
    # model = Product
    # fields = ['name', 'product_type', 'description', 'short_desc', 'stock', 'original_price', 'sale_price', 'active']
