from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.http import HttpResponse
from WebSite.products.models import ProductType, Product
from django.db.models import Q

#########################
# Misc
def index(request):
    return render(request, "misc/index.html")


def list_products(request):
    if request.method == 'GET' and 'search' in request.GET:
        texto = request.GET.get("search", "")
        products = searchALLActiveArtesaoCriativos(texto)

    else:
        products = Product.objects.filter(active=True, stock__gte=1)
    return render(request, 'home.html', {'products': products})  # alterar para o html de listagem


# def search_products(request):
# products = request.GET.get('search')
# return render(request, '../templates/store/home.html', {'products': products})


def search_products(request):
    # import pdb; pdb.set_trace()
    query = request.GET.get('search')
    if query:
        products = Product.objects.filter(name=query)
    return render(request, 'home.html', {"products": products})


def product(request):
    return render(request, "product_page.html")

def searchALLActiveArtesaoCriativos(texto):
   listaProducts = Product.objects.filter(Q(active=True),
                                        Q(description__icontains=texto) | Q(name__icontains=texto))
   listaP = list(listaProducts)
   return listaP