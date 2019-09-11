from django import forms
from .models import Product, MakerProduct


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    crafters=forms.CharField(max_length=250)
    # class Meta:
    # model = Product
    # fields = ['name', 'product_type', 'description', 'short_desc', 'stock', 'original_price', 'sale_price', 'active']
