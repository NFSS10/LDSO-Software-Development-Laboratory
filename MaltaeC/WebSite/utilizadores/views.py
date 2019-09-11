import os
from django.shortcuts import render
from django.contrib.auth.models import User
from passlib.hash import pbkdf2_sha256  # pip install passlib
from .forms import LoginForm, RegisterForm, RegisterArtesaoForm, EditUserProfileForm, EditArtistProfileForm, \
    ResetPasswordForm, ResetPasswordConfirmForm
from .models import SettingsBackend, BaseUser, Criativo, Artesao, Utilizador, PropostaRegisto, ImageUser
from WebSite.events.models import Event
from WebSite.administrador.models import Entrevista, EmailsBanidos
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import cache
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from WebSite.cart.models import Cart
from WebSite.tools.models import Tool
import re
import math
import operator
from django.db.models.query import QuerySet
from django.db.models import Q
import requests



def getCidadeByLatLong(lat, long):
    data = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+","+str(long)+"&key=AIzaSyAnZC9JhRA88UOd2yTiLQeWbxfvYm7A_vc").json()
    jsonlist = data["results"]
    try:
        cidade = jsonlist[0]["address_components"][4]["long_name"]
    except IndexError:
        cidade = ""

    return cidade



def register(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('/home')

    if request.method == 'POST':
        if 'maker-submit' in request.POST:
            registerForm = RegisterArtesaoForm(request.POST)
            if registerForm.is_valid():
                formData = registerForm.cleaned_data

                if EmailsBanidos.objects.filter(email=formData["email"]).exists():
                    return render(request, "registo.html", {'success': 'invalid', 'erroMsg': 'Email Banido'})

                if BaseUser.objects.filter(email=formData["email"]).exists():
                    return render(request, "registo.html", {'success': 'invalid', 'erroMsg': 'Email ja existe'})
                else:
                    pwd = formData["password"]
                    c_pwd = formData["password_confirm_maker"]
                    if pwd == c_pwd:
                        if request.POST.get("choiceType") == 'criativo':
                            if 'test-envtest' in request.POST:
                                urlImg = "testeimgurl"
                            else:
                                if Criativo.objects.count() == 0:
                                    urlImg = uploadImage("/userPics/" + str(0),
                                                         "registoProposta",
                                                         request.FILES['imgProposta'])
                                else:
                                    urlImg = uploadImage("/userPics/" + str(int(Criativo.objects.latest('id').id) + 1),
                                                         "registoProposta",
                                                         request.FILES['imgProposta'])

                            pattern = re.compile("^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$")
                            ytvideoURL = request.POST.get("videoURL")
                            if pattern.match(ytvideoURL):
                                ytvideoURL = ytvideoURL.replace("watch?v=", "embed/")
                            else:
                                ytvideoURL = ""

                            categorias = request.POST.getlist('categorias[]', "")
                            catStr = ""
                            for categoria in categorias:
                                catStr = catStr + categoria + "+"

                            proposta = PropostaRegisto(texto=formData["areatexto"],
                                                       imgUrl=urlImg,
                                                       videoUrl=ytvideoURL)
                            proposta.save()
                            cidade = getCidadeByLatLong(formData["latitude"], formData["longitude"])
                            criativo = Criativo(email=formData["email"], password=pwd,
                                                name=formData["username"], geolocation=formData["geolocation"],
                                                latitude=formData["latitude"], longitude=formData["longitude"],
                                                phoneNumber=formData["phone_maker"],
                                                type="criativo",
                                                is_active=False,
                                                propostaRegisto=proposta,
                                                categorias=catStr,
                                                cidade=cidade)
                            criativo.set_password(pwd)
                            criativo.save()
                            cart = Cart(user=criativo)
                            cart.save()
                            return render(request, "registo.html", {'success': 'success'})


                        elif request.POST.get("choiceType") == 'artesao':

                            if 'test-envtest' in request.POST:
                                urlImg = "testeimgurl"
                            else:
                                if Artesao.objects.count() == 0:
                                    urlImg = uploadImage("/userPics/" + str(0),
                                                         "registoProposta",
                                                         request.FILES['imgProposta'])
                                else:
                                    urlImg = uploadImage("/userPics/" + str(int(Artesao.objects.latest('id').id) + 1),
                                                         "registoProposta",
                                                         request.FILES['imgProposta'])

                            pattern = re.compile("^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$")
                            ytvideoURL = request.POST.get("videoURL")
                            if pattern.match(ytvideoURL):
                                ytvideoURL = ytvideoURL.replace("watch?v=", "embed/")
                            else:
                                ytvideoURL = ""

                            categorias = request.POST.getlist('categorias[]', "")

                            catStr = ""
                            for categoria in categorias:
                                catStr = catStr + categoria + "+"

                            proposta = PropostaRegisto(texto=formData["areatexto"],
                                                       imgUrl=urlImg,
                                                       videoUrl=ytvideoURL)
                            proposta.save()
                            cidade = getCidadeByLatLong(formData["latitude"], formData["longitude"])
                            artesao = Artesao(email=formData["email"], password=pwd,
                                              name=formData["username"], geolocation=formData["geolocation"],
                                              latitude=formData["latitude"], longitude=formData["longitude"],
                                              phoneNumber=formData["phone_maker"],
                                              type="artesao",
                                              is_active=False,
                                              propostaRegisto=proposta,
                                              categorias=catStr,
                                              cidade = cidade)
                            artesao.set_password(pwd)
                            artesao.save()
                            cart = Cart(user=artesao)
                            cart.save()
                            return render(request, "registo.html", {'success': 'success'})
                        else:
                            return render(request, "registo.html",
                                          {'success': 'invalid', 'erroMsg': 'Erro na selecao do tipo'})
                    else:
                        return render(request, "registo.html", {'erroMsg': 'Senhas diferentes'})
            else:  # Form invalido
                return render(request, "registo.html",
                              {'success': 'invalid', 'erroMsg': 'Erro nos valores, formulario invalido'})


        elif 'regular-submit' in request.POST:
            registerForm = RegisterForm(request.POST)
            if registerForm.is_valid():
                formData = registerForm.cleaned_data

                if EmailsBanidos.objects.filter(email=formData["email_regular"]).exists():
                    return render(request, "registo.html", {'success': 'invalid', 'erroMsg': 'Email Banido'})

                if BaseUser.objects.filter(email=formData["email_regular"]).exists():
                    return render(request, "registo.html", {'success': 'invalid', 'erroMsg': 'Email ja existe'})
                else:
                    pwd = formData["password_regular"]
                    c_pwd = formData["password_confirm_regular"]
                    if pwd == c_pwd:
                        utilizador = Utilizador(
                            email=formData["email_regular"], password=pwd,
                            name=formData["username_regular"], phoneNumber=formData["phone_regular"],
                            adress=formData["address_regular"],
                            type="utilizador"
                        )
                        utilizador.set_password(pwd)
                        utilizador.save()
                        cart = Cart(user=utilizador)
                        cart.save()
                        return render(request, "registo.html", {'success': 'success'})
                    else:
                        return render(request, "registo.html", {'erroMsg': 'Senhas diferentes'})
            else:  # Form invalido
                return render(request, "registo.html", {'success': 'invalid', 'erroMsg': 'Erro nos valores'})
        else:
            return render(request, "registo.html", {'success': 'invalid', 'erroMsg': 'Erro inesperado'})
    return render(request, "registo.html")


@csrf_exempt
def loginView(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            formData = loginForm.cleaned_data
            mail = formData["username"]
            pwd = formData["password"]
            user = SettingsBackend.authenticate(request, email=mail, password=pwd)
            if user is not None:
                if user.is_active or (user.is_active is False and user.reprovado):
                    login(request, user)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                elif user.is_active is False and user.reprovado is False:
                    return loginFormView(request, "Utilizador a guardar aprovacao")
            else:
                return loginFormView(request, "Email ou Password incorretos")
    return loginFormView(request)


@csrf_exempt
def loginFormView(request, errorMsg=None):
    if request.user.is_authenticated:
        return redirect('/home')
    return render(request, "loginForm.html", {'errorMsg': errorMsg})


def logoutView(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def viewProfile(request):
	id = request.GET.get("id", "none")
	if id == "none":
		if request.user.is_authenticated:
			if Event.objects.filter(creator=int(request.user.id)).exists():
				eventsList = Event.objects.filter(creator=int(request.user.id))
			else:
				eventsList = "noEvents"
			if Entrevista.objects.filter(userID=int(request.user.id)).exists():
				entrevista = Entrevista.objects.filter(userID=int(request.user.id)).get()
			else:
				entrevista = "noEntrevista"
			return render(request, "profile.html",{'userInfo': request.user, 'eventsList': eventsList, 'entrevista': entrevista})
		else:
			return redirect('/home')
	else:
		idUser = int(id)
		if BaseUser.objects.filter(id=idUser).exists():
			user = BaseUser.objects.filter(id=idUser).get()
			if Event.objects.filter(creator=idUser).exists():
				eventsList = Event.objects.filter(creator=idUser)
			else:
				eventsList = "noEvents"
			if Tool.objects.filter(userId=idUser).exists():
				tools = Tool.objects.filter(userId=idUser)
			else:
				tools = "noTools"
			if Entrevista.objects.filter(userID=idUser).exists():
				entrevista = Entrevista.objects.filter(userID=idUser).get()
			else:
				entrevista = "noEntrevista"
			if ImageUser.objects.filter(userEmail=user.email).exists():
				images = ImageUser.objects.filter(userEmail=user.email)
			else:
				images = "noImages"
			if user.type == "artesao" or user.type == "criativo":
				listaCategorias = user.categorias.split("+")
			else:
				listaCategorias = "noCategorias"
			return render(request, "profile.html",{'userInfo': user, 'eventsList': eventsList, 'entrevista': entrevista, 'images': images,'tools': tools, 'listaCategorias': listaCategorias})
		else:
			return redirect('/home')


def edit_profile(request, errorMsgs=None, infoMsgs=None, default="info"):
    if request.user.is_authenticated:
        images = ImageUser.objects.filter(userEmail=request.user.email)
        nImages = images.count()
        tools = Tool.objects.filter(userId=request.user.id)
        toolsRange = range(math.ceil(tools.count() / 3))
        nTools = tools.count()
        return render(request, "edit-user-profile.html",
                      {'errorMsgs': errorMsgs, 'infoMsgs': infoMsgs, 'default': default, 'images': images,
                       'nImages': nImages, 'tools': tools, 'toolsRange': toolsRange, 'nTools': nTools})
    else:
        return loginFormView(request)


@csrf_exempt
def edit_profile_action(request):
    errorMsgs = []
    infoMsgs = []
    if request.method == 'POST' and request.user.is_authenticated:
        if request.user.type == "utilizador":
            editProfileForm = EditUserProfileForm(request.POST)
        else:
            editProfileForm = EditArtistProfileForm(request.POST)
        if editProfileForm.is_valid():
            formData = editProfileForm.cleaned_data
            # nome
            user = BaseUser.objects.filter(email=request.user.email).get()
            if formData["name"] is not "":
                user.name = formData["name"]
                request.user.name = formData["name"]
                infoMsgs.append("- Nome atualizado com sucesso!")
            # password
            if formData["old_password"] is not "" or formData["new_password"] is not "":
                if not ((formData["old_password"] is not "" and formData["new_password"] is "") or (
                        formData["old_password"] is "" and formData["new_password"] is not "")):
                    if user.check_password(formData["old_password"]):
                        user.set_password(formData["new_password"])
                        logout(request)
                        login(request, user)
                        infoMsgs.append("- Password atualizada com sucesso!")
                    else:
                        errorMsgs.append("- Password atual errada")
                else:
                    errorMsgs.append("- Preencha ambos os campos password.")
            # bio
            if formData["bio"] is not "":
                user.bio = formData["bio"]
                request.user.bio = formData["bio"]
                user.save()
                infoMsgs.append("- Biografia atualizada com sucesso!")
            # phonenumber
            if formData["phone_number"] is not "":
                if formData["phone_number"].isdigit():
                    user.phoneNumber = formData["phone_number"]
                    request.user.phoneNumber = formData["phone_number"]
                    infoMsgs.append("- Numero atualizado com sucesso!")
                else:
                    errorMsgs.append("- Numero de telefone apenas pode conter digitos.")
            # Adress
            if user.type == "utilizador":
                if formData["adress"] is not "":
                    user.utilizador.adress = formData["adress"]
                    request.user.utilizador.adress = formData["adress"]
                    user.utilizador.save()
                    infoMsgs.append("- Morada atualizada com sucesso!")
            # localization
            if user.type == "criativo":
                if formData["latitude"] is not None and formData["longitude"] is not None:
                    user.criativo.geolocation = formData["geolocation"]
                    user.criativo.latitude = formData["latitude"]
                    user.criativo.longitude = formData["longitude"]
                    request.user.criativo.geolocation = formData["geolocation"]
                    request.user.criativo.latitude = formData["latitude"]
                    request.user.criativo.longitude = formData["longitude"]
                    user.criativo.save()
                    infoMsgs.append("- Localizacao atualizada com sucesso!")
            if user.type == "artesao":
                if formData["latitude"] is not None and formData["longitude"] is not None:
                    user.artesao.geolocation = formData["geolocation"]
                    user.artesao.latitude = formData["latitude"]
                    user.artesao.longitude = formData["longitude"]
                    request.user.artesao.geolocation = formData["geolocation"]
                    request.user.artesao.latitude = formData["latitude"]
                    request.user.artesao.longitude = formData["longitude"]
                    user.artesao.save()
                    infoMsgs.append("- Localizacao atualizada com sucesso!")
            # -------------------------
            user.save()
            if len(errorMsgs) == 0:
                infoMsgs = []
                infoMsgs.append("- Valores atualizados com sucesso!")
            return edit_profile(request, errorMsgs, infoMsgs)
        else:
            errorMsgs.append("- Erro de formulario, verifique os campos.")
            return edit_profile(request, errorMsgs, infoMsgs)
    else:
        return redirect('/home', foo='bar')


# Usage: uploadImage("/folder1/subfolder/example", "imgNameWanted", imgFile)
# returns url to file
def uploadImage(pathToFolder, name, ImgFile, profile=1):
    folder = settings.MEDIA_ROOT + pathToFolder
    try:
        os.makedirs(folder)
    except:
        pass
    fs = FileSystemStorage()
    if profile is 1:

        fileName, fileExtension = ImgFile.name.rsplit(".", 1)
        try:
            os.remove(folder + "/" + name + "." + fileExtension)
        except:
            pass
        path = fs.save(folder + "/" + name + "." + fileExtension, ImgFile)

        imgURL = "media" + pathToFolder + "/" + name + "." + fileExtension
    else:
        path = fs.save(folder + "/" + ImgFile.name, ImgFile)
        imgURL = "media/" + os.path.relpath(path, settings.MEDIA_ROOT)
    return imgURL


@csrf_exempt
def change_user_video(request):
    if request.method == 'POST' and request.user.is_authenticated:
        pattern = re.compile("^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$")
        ytvideoURL = request.POST['videoUrl']
        if pattern.match(ytvideoURL):
            infoMsgs = []
            infoMsgs.append("Video alterado com sucesso!")
            ytvideoURL = ytvideoURL.replace("watch?v=", "embed/")
            user = BaseUser.objects.filter(email=request.user.email).get()
            user.videoUrl = ytvideoURL
            request.user.videoUrl = ytvideoURL
            user.save()
            return edit_profile(request, errorMsgs=None, infoMsgs=infoMsgs, default="multimedia")
        else:
            errorMsgs = []
            errorMsgs.append("Insira um link Youtube valido.")
            return edit_profile(request, errorMsgs=errorMsgs, default="multimedia")
    else:
        return redirect('/home', foo='bar')


def upload_5Image(request):
    if request.method == 'POST' and request.user.is_authenticated:
        images = ImageUser.objects.filter(userEmail=request.user.email)
        nImages = images.count()
        if nImages <= 4:
            infoMsg = []
            infoMsg.append("Imagem adicionada a galeria.")
            imgurl = uploadImage("/userPics/" + str(request.user.id), request.FILES['5image'].name,
                                 request.FILES['5image'], 0)
            image = ImageUser(userEmail=request.user.email, imgUrl=imgurl)
            image.save()
            return edit_profile(request, infoMsgs=infoMsg, default="multimedia")
        else:
            errorMsgs = []
            errorMsgs.append("Ja possui o numero maximo de imagens, apague uma para voltar a carregar.")
            return edit_profile(request, errorMsgs=errorMsgs, default="multimedia")
    else:
        return redirect('/home', foo='bar')


def delete_5Image(request):
    if request.method == 'POST' and request.user.is_authenticated:
        infoMsg = []
        infoMsg.append("Imagem apagada com sucesso.")

        os.remove(request.POST['imgurl'])
        image = ImageUser.objects.filter(imgUrl=request.POST['imgurl'])
        image.delete()
        return edit_profile(request, infoMsgs=infoMsg, default="multimedia")
    else:
        return redirect('/home', foo='bar')


def upload_image_view(request):
    if request.method == 'POST':
        infoMsg = []
        infoMsg.append("Foto de perfil alterada com sucesso!")

        imgUrl = uploadImage("/userPics/" + str(request.user.id),
                             "profilePic",
                             request.FILES['img'])

        user = BaseUser.objects.filter(email=request.user.email).get()
        user.picUrl = imgUrl
        request.user.picUrl = imgUrl
        user.save()
        return edit_profile(request, infoMsgs=infoMsg, default="multimedia")
    else:
        return redirect('/home', foo='bar')


def resetPasswordConfirmView(request, uidb64=None, token=None):
    assert uidb64 is not None and token is not None
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = BaseUser._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, BaseUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordConfirmForm(request.POST)
            if form.is_valid():
                formData = form.cleaned_data
                if formData["new_password"] == formData["new_password_confirm"]:
                    user.set_password(formData["new_password"])
                    user.save()
                    return render(request, "reset-password-confirm.html", {'infoMsg': "Password alterada com sucesso."})
                else:
                    return render(request, "reset-password-confirm.html", {'errorMsg': "Passwords nao coincidem."})
        else:
            return render(request, "reset-password-confirm.html")
    else:
        return render(request, "reset-password-confirm.html", {'expMsg': "Este link encontra-se expirado"})


def resetPasswordInsertView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':  # envia email e da redirect para a proxima pagina
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                formData = form.cleaned_data
                if BaseUser.objects.filter(email=formData["email"]).exists():
                    user = BaseUser.objects.filter(email=formData["email"]).get()
                    c = {'email': user.email, 'domain': request.META['HTTP_HOST'],
                         'site_name': 'Malta e Companhia Website', 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                         'user': user, 'token': default_token_generator.make_token(user), 'protocol': 'http', }
                    subject_template_name = 'password_reset_subject.txt'
                    email_template_name = 'password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                    infoMsg = "Pedido de reset de password enviado para o email."
                    return render(request, "reset-password-insert.html", {'infoMsg': infoMsg})
                else:
                    errorMsg = "Email nao existente."
            else:
                errorMsg = "Email nao valido"
            return render(request, "reset-password-insert.html", {'errorMsg': errorMsg})
        else:
            return render(request, "reset-password-insert.html")
    else:
        return redirect('/home', foo='bar')


def getAllActiveCriativos():
    if Criativo.objects.filter(is_active=True).count() > 0:
        return Criativo.objects.filter(is_active=True)
    else:
        return "noCriativos"


def getAllActiveArtesao():
    if Artesao.objects.filter(is_active=True).count() > 0:
        return Artesao.objects.filter(is_active=True)
    else:
        return "noArtesao"


def getALLActiveArtesaoCriativos():
    artList = getAllActiveArtesao()
    criList = getAllActiveCriativos()

    if isinstance(artList, QuerySet) and isinstance(criList, QuerySet):
        artList = artList.order_by('name')
        criList = criList.order_by('name')
        listaCompleta = list(artList) + list(criList)

        return listaCompleta
    elif isinstance(artList, QuerySet):
        artList = artList.order_by('name')
        artList = list(artList)

        return artList
    elif isinstance(criList, QuerySet):
        criList = criList.order_by('name')
        criList = list(criList)

        return criList
    else:
        listaVazia = ""
        listaVazia = list(listaVazia)
        return listaVazia


def searchALLActiveArtesaoCriativos(texto):
    listaUsers = BaseUser.objects.filter(Q(is_active=True),
                                         Q(type="artesao") | Q(type="criativo"),
                                         Q(categorias__icontains=texto) | Q(name__icontains=texto) | Q(cidade__icontains=texto))
    listaUsers = list(listaUsers)
    return listaUsers


def verTodosArtesaosCriativos(request):
    if request.method == 'GET' and 'search' in request.GET:
        listaCompleta = searchArtesaos(request)

        if listaCompleta == "":
            listaCompleta = getALLActiveArtesaoCriativos()
            for user in listaCompleta:
                catg = user.categorias.split("+")
                user.categorias = str(catg[0])

            return render(request, "artesaos.html", {'listaArtesaosCriativos': listaCompleta})
        elif listaCompleta == "nada":
            return render(request, "artesaos.html", {'listaArtesaosCriativos': listaCompleta, 'pesquisa': "vazio"})
        else:
            for user in listaCompleta:
                catg = user.categorias.split("+")
                user.categorias = str(catg[0])

            return render(request, "artesaos.html", {'listaArtesaosCriativos': listaCompleta})
    else:
        listaCompleta = getALLActiveArtesaoCriativos()
        for user in listaCompleta:
            catg = user.categorias.split("+")
            user.categorias = str(catg[0])

    return render(request, "artesaos.html", {'listaArtesaosCriativos': listaCompleta})


def searchArtesaos(request):
    textoPesquisa = request.GET.get("search", "")
    if textoPesquisa == "":
        return ""

    listaUsers = searchALLActiveArtesaoCriativos(textoPesquisa)

    if not listaUsers:
        return "nada"
    else:

        return listaUsers
