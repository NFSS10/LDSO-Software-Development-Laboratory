from django.shortcuts import render
from django.http import HttpResponse
from .forms import CartForm
from django.db import transaction
from WebSite.utilizadores.models import BaseUser
from WebSite.products.models import Product
from .models import Cart, CartItem
from WebSite.products.views import show_product


# Create your views here.
#
def add_productCart(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CartForm(request.POST)
            if form.is_valid():
                cart = Cart.objects.get(user_id=request.user.id)

                product = Product.objects.get(pk=form.cleaned_data['product'])
                item = CartItem(cart=cart, product=product, quantidade=form.cleaned_data['quantidade'])
                item.save()

                return show_product(request,product.pk)  # descobrir como redirecionar para a mesma pagina
    return render(request, 'cartPage.html')  # descobrir como redirecionar para a mesma pagina


def remove_fromCart(request, cartItemid):
    if request.user.is_authenticated:
        CartItem.objects.get(pk=cartItemid).delete()
        # product = Product.objects.get(pk=form.cleaned_data['product'])
        # CartItem.objects.filter(cart=cartid, product=product).delete()

    return show_cart(request)  # descobrir como redirecionar para a mesma pagina


def show_cart(request):
    if request.user.is_authenticated:
        # products = []
        cartid = Cart.objects.get(user_id=request.user.id)
        items = CartItem.objects.filter(cart=cartid)
        sum = 0;
        for item in items:
            sum += item.product.original_price
        return render(request, 'cartPage.html', {'items': items, 'sum': sum})
    return render(request, 'home.html')
