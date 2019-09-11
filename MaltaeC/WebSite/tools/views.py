import os
from .models import Tool
from django.shortcuts import render
from WebSite.utilizadores.views import uploadImage, edit_profile
from WebSite.utilizadores.models import BaseUser
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import redirect
import operator
from django.db.models.query import QuerySet
from django.db.models import Q
# Create your views here.
#

def addToolView(request):
	if request.user.is_authenticated:
		if request.user.type == "criativo" or request.user.type == "artesao":
			if request.method == 'POST':
				nomeFerramenta = request.POST['nomeFerramenta']
				descricaoFerramenta = request.POST['descFerramenta']
				precoFerramenta = request.POST['precoFerramenta']
				imagemFerramenta = request.FILES['imgFerramenta']
				imagemUrl = uploadImage("/userPics/" + str(request.user.id) + "/tools",imagemFerramenta.name,imagemFerramenta,0)
				tool = Tool(userId = request.user.id, name = nomeFerramenta, description = descricaoFerramenta, imageUrl = imagemUrl, price= precoFerramenta )
				tool.save()
				messages.success(request, 'Ferramenta adicionada com sucesso')
				return redirect(edit_profile, default='ferramentas')
	return redirect("/home")
	
def deleteToolView(request):
	if request.user.is_authenticated:
		if request.user.type == "criativo" or request.user.type == "artesao":
			if request.method == 'POST':
				tool = Tool.objects.filter(id=request.POST['toolId']).get()
				tool.delete()
				os.remove(tool.imageUrl)
				messages.success(request, 'Ferramenta apagada com sucesso')
				return redirect(edit_profile, default='ferramentas')
	return redirect("/home")
	
def toolProfileView(request):
	toolId = request.GET.get("id", "none")
	if id == "none":
		return redirect("/home")
	else:
		toolId= int(toolId)
		if Tool.objects.filter(id = toolId).exists():
			tool = Tool.objects.filter(id = toolId).get()
			user = BaseUser.objects.filter(id = tool.userId).get()
			return render(request, "toolProfile.html", {'tool': tool, 'user': user})
		else:
			return redirect("/home")

def searchAllTools(texto):
	toolsList = Tool.objects.filter(Q(name__icontains=texto) | Q(description__icontains=texto))
	toolsList = list(toolsList)
	return toolsList

			
			
def searchTools(request):
	textoPesquisa = request.GET.get("search", "")
	if textoPesquisa == "":
		return ""

	toolsList = searchAllTools(textoPesquisa)

	if not toolsList:
		return "nada"
	else:

		return toolsList
			
def listToolsView(request):

	if request.method == 'GET' and 'search' in request.GET:
		toolsList = searchTools(request)
		if toolsList == "":
			toolsList = Tool.objects.all()
			return render(request, "tools.html", {'listaTools': toolsList})
		else:
			return render(request, "tools.html", {'listaTools': toolsList})
	
	else:
		toolsList = Tool.objects.all()
		return render(request, "tools.html", {'listaTools': toolsList})