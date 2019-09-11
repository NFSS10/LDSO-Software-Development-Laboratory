#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from .models import EmailsBanidos, Entrevista, CarouselIMGs
from django.conf import settings


from WebSite.utilizadores.models import BaseUser, Criativo, Artesao, Utilizador
from WebSite.utilizadores.views import uploadImage

def manage(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            listaCritativoInativos = Criativo.objects.filter(Q(is_active=False) & Q(reprovado=False))
            listaArtesaoInativos = Artesao.objects.filter(Q(is_active=False) & Q(reprovado=False))


            return render(request, "administrador.html", {'listaCritativoInativos': listaCritativoInativos, 'listaArtesaoInativos': listaArtesaoInativos})
        else:
            return redirect('/home')
    else:
        return redirect('/home')

def desbanirUser(request):
	if request.user.is_authenticated:
		if request.user.is_staff:
			if request.method == 'POST':
				email = request.POST['email']
				emailObj = EmailsBanidos.objects.get(email=email)
				emailObj.delete()
		emails= EmailsBanidos.objects.all()
		return 	render(request, "emailsBanidos.html", {'emails': emails})
	return redirect('/home')

def aprovarUser(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                user = BaseUser.objects.filter(id=int(request.POST.get("id", ""))).get()
                user.is_active = True
                user.reprovado = False
                user.save()
                return manage(request)
            else:
                return manage(request)
        else:
            return redirect('/home')
    else:
        return redirect('/home')


def reprovarUser(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                user = BaseUser.objects.filter(id=int(request.POST.get("id", ""))).get()
                user.is_active = False
                user.reprovado = True
                user.save()
                return validarReprovado(request)
            else:
                return validarReprovado(request)
        else:
            return redirect('/home')
    else:
        return redirect('/home')


def banirUser(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                user = BaseUser.objects.filter(id=int(request.POST.get("id", ""))).get()
                email = user.email
                emailbanido = EmailsBanidos(email=email)
                emailbanido.save()
                user.delete()
                return manage(request)
            else:
                return manage(request)
        else:
            return redirect('/home')
    else:
        return redirect('/home')


#HTML onde cria a entrevista e depois chama o add
def criarEntrevista(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                userID = int(request.POST.get("idEntrevista", ""))
                return render(request, "criarEntrevista.html", {'idEntrevista': userID})
            else:
                return redirect("/utilizadores/login")
        else:
            return redirect("/utilizadores/login")
    else:
        return redirect("/utilizadores/login")




def addEntrevista(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                userID = int(request.POST.get("idEntrevista", ""))
                conteudo = request.POST.get("conteudoEntrevista", "")


                if Entrevista.objects.filter(userID = userID).exists():
                    entrevista = Entrevista.objects.filter(userID = userID).get()
                    entrevista.delete()
                    entrevista = Entrevista(userID = BaseUser.objects.filter(id=userID).get(),
                                            conteudoEntrevista = conteudo)
                    entrevista.save()
                else:
                    entrevista = Entrevista(userID=BaseUser.objects.filter(id=userID).get(),
                                            conteudoEntrevista=conteudo)
                    entrevista.save()
                return redirect("/utilizadores/perfil?id="+str(userID))
            else:
                return redirect("/utilizadores/login")
        else:
            return redirect("/utilizadores/login")
    else:
        return redirect("/utilizadores/login")



def validarReprovado(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            listaCritativoReprovados = Criativo.objects.filter(reprovado=True)
            listaArtesaoReprovados = Artesao.objects.filter(reprovado=True)

            return render(request, "reprovados.html", {'listaCritativoReprovados': listaCritativoReprovados, 'listaArtesaoReprovados': listaArtesaoReprovados})
        else:
            return redirect('/home')
    else:
        return redirect('/home')




def mudarCarousel(request):
    carouselIMGs = CarouselIMGs.objects.filter(id = 1).get()
    if request.method == 'POST':
        if request.FILES.get('img1',False):
            urlImg1 = uploadImage("/index_carousel", "1", request.FILES['img1'])
            carouselIMGs.img1 = urlImg1
        if request.FILES.get('img2',False):
            urlImg2 = uploadImage("/index_carousel", "2", request.FILES['img2'])
            carouselIMGs.img2 = urlImg2
        if request.FILES.get('img3',False):
            urlImg3 = uploadImage("/index_carousel", "3", request.FILES['img3'])
            carouselIMGs.img3 = urlImg3
        if request.FILES.get('img4',False):
            urlImg4 = uploadImage("/index_carousel", "4", request.FILES['img4'])
            carouselIMGs.img4 = urlImg4
        if request.FILES.get('img5',False):
            urlImg5 = uploadImage("/index_carousel", "5", request.FILES['img5'])
            carouselIMGs.img5 = urlImg5

        carouselIMGs.save()
        return render(request, "mudarIndexCarousel.html", {'carouselIMGs': carouselIMGs})
    else:
        return render(request, "mudarIndexCarousel.html", {'carouselIMGs': carouselIMGs})



def registarAdmin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':

            if BaseUser.objects.filter(email=request.POST.get("email")).exists():
                return render(request, "addAdmin.html", {'erroMsg': "Email já registado"})

            pwd = request.POST.get("pwd")
            c_pwd = request.POST.get("cpwd")

            if pwd == c_pwd:
                admin = BaseUser(email=request.POST.get("email"), name=request.POST.get("nome"),
                                 phoneNumber=request.POST.get("telefone"),password=pwd,
                                 is_active=True, is_staff=True)
                admin.set_password(pwd)
                admin.save()
                return render(request, "addAdmin.html", {'sucessoMsg': "Novo Admin registado"})
            else:
                return render(request, "addAdmin.html", {'erroMsg': "Passwords não coincidem"})
        else:
            return render(request, "addAdmin.html")
    else:
        return manage(request)




def verTodosUsers(request):
    if request.user.is_authenticated and request.user.is_staff:
        listaCritativos = Criativo.objects.all()
        listaArtesaos = Artesao.objects.all()
        listaClientes = Utilizador.objects.all()

        if request.user.is_superuser:
            listaAdmins = BaseUser.objects.filter(is_staff=True, is_superuser=False)
            return render(request, "verTodosUsers.html", {'listaCriativos': listaCritativos, 'listaArtesaos': listaArtesaos, 'listaClientes': listaClientes, 'listaAdmins': listaAdmins})
        return render(request, "verTodosUsers.html", {'listaCriativos': listaCritativos, 'listaArtesaos': listaArtesaos, 'listaClientes': listaClientes})
    else:
        return manage(request)
