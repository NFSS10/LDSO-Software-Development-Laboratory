from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductForm
from django.db import transaction
from .models import ProductType, Product, MakerProduct
from WebSite.utilizadores.models import Criativo, Artesao, BaseUser


# Create your views here.
#

@transaction.atomic
def register_product(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                m = Product(name=form.cleaned_data['name'],
                            description=form.cleaned_data['description'],
                            short_desc=form.cleaned_data['short_desc'],
                            stock=form.cleaned_data['stock'],
                            original_price=form.cleaned_data['original_price'],
                            sale_price=form.cleaned_data['sale_price'],
                            active=True,
                            image=form.cleaned_data['image'])

                m.save()
                list = form.cleaned_data['crafters']
                for makerid in list.split(" "):
                    link = MakerProduct(product=m, maker=BaseUser.objects.get(pk=int(makerid)))
                    link.save()
                return list_products(request)


# ask if this is used


def list_products(request):
    if request.method == 'GET' and 'search' in request.GET:
        texto = request.GET.get("search", "")
        products = searchALLActiveArtesaoCriativos(texto)

    else:
        products = Product.objects.filter(active=True, stock__gte=1)
    return render(request, 'home.html', {'products': products})  # alterar para o html de listagem


def show_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    association = MakerProduct.objects.filter(product_id=product_id)
    responsibles = []
    for responsible in association:
        responsibles.append(BaseUser.objects.get(pk=responsible.maker_id))
    return render(request, 'product_page.html', {'product': product, 'responsibles': responsibles})


def add_product(request):
    if request.user.is_authenticated and request.user.is_staff:
        criativos = Criativo.objects.all()

        list = []
        for artesao in Artesao.objects.all():
            info = [artesao.baseuser_ptr_id, BaseUser.objects.get(pk=artesao.baseuser_ptr_id).name]
            list.append(info)
        for criativo in criativos:
            info = [criativo.baseuser_ptr_id, BaseUser.objects.get(pk=criativo.baseuser_ptr_id).name]
            list.append(info)
        return render(request, 'add_product.html', {'list': list})
    else:
        return render(request, 'home.html')


def manage_products(request):
    if request.user.is_authenticated and request.user.is_staff:
        products = Product.objects.all()
        return render(request, 'ManageProducts.html', {'products': products})


def deactivateProduct(request, product_id):
    if request.user.is_authenticated and request.user.is_staff:
        Product.objects.filter(pk=product_id).update(active=False)
        products = Product.objects.all()
        return render(request, 'ManageProducts.html', {'products': products})


def activateProduct(request, product_id):
    if request.user.is_authenticated and request.user.is_staff:
        Product.objects.filter(pk=product_id).update(active=True)
        products = Product.objects.all()
        return render(request, 'ManageProducts.html', {'products': products})


def searchALLActiveArtesaoCriativos(texto):
   listaProducts = Product.objects.filter(Q(active=True),
                                        Q(description__icontains=texto) | Q(name__icontains=texto))
   listaP = list(listaProducts)
   return listaP