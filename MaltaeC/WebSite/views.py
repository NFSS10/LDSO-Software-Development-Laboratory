from django.shortcuts import get_object_or_404, render
from WebSite.utilizadores.views import getAllActiveArtesao, getAllActiveCriativos
from WebSite.administrador.models import CarouselIMGs
from WebSite.products.models import ProductType, Product
from WebSite.tools.models import Tool
from WebSite.events.models import Event
from WebSite.utilizadores.models import Criativo, Artesao
from django.conf import settings
from django.core import mail


#########################
#Misc
def index(request):
	artList = getAllActiveArtesao()
	criList = getAllActiveCriativos()
	products = Product.objects.all()[:5]
	tools = Tool.objects.all()[:5]
	events = Event.objects.all()[:5]
	criativos = Criativo.objects.filter(is_active=True)[:3]
	artesaos = Artesao.objects.filter(is_active=True)[:3]

	if CarouselIMGs.objects.count() < 1:
		carousel = CarouselIMGs()
		carousel.save()
	else:
		carousel = CarouselIMGs.objects.filter(id = 1).get
		return render(request, "misc/index.html", {'artesaosList': artList, 'criativosList': criList, 'carousel': carousel, 'products': products, 'tools':tools, 'events': events, 'criativos':criativos, 'artesaos':artesaos})
	return render(request, "misc/index.html",{'artesaosList': artList, 'criativosList': criList, 'carousel': carousel, 'products': products, 'tools':tools, 'events': events, 'criativos':criativos, 'artesaos':artesaos})


def sobre(request):
	return render(request, "misc/sobre.html")

def contactMe(request):
	if request.method == 'POST':
		connection = mail.get_connection()
		connection.open()

		nome = request.POST.get("nome")
		fromEmail = request.POST.get("email")
		msg = request.POST.get("areatexto")

		emailToSend = mail.EmailMessage(
			"Mensagem de "+nome + " ["+fromEmail+"]",
			msg,
			fromEmail,
			[settings.DEFAULT_FROM_EMAIL],
			connection=connection,
			reply_to=[fromEmail]
		)
		emailToSend.send()  # Send the email
		return render(request, "misc/contact_me.html", {'sucessoMSG': "Mensagem enviada !"})
	else:
		return render(request, "misc/contact_me.html")

def list_products(request):
    products = Product.objects.all()
    return render(request, 'misc/index.html', {'products': products})


##def store(request):
    #return render(request,"store/home.html")

#def product(request):
    #return render(request,"products/product_page.html")
