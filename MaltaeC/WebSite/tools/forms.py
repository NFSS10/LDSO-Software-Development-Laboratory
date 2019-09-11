from django import forms
from .models import Product


class ToolsForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = '__all__'
        file = forms.ImageField()
    
    
    #class Meta:
        #model = Product
        #fields = ['name', 'product_type', 'description', 'short_desc', 'stock', 'original_price', 'sale_price', 'active']