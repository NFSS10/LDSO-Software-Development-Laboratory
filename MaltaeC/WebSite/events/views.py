#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template import loader
from django.db import transaction
from .forms import EventForm, EventRegisterUser, EditEventForm, SearchForm, MailForm
from WebSite.utilizadores.models import Utilizador
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from .models import Event, EventType, EventParticipation, TutorEvent, EventImages
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from PIL import Image
import json


#TODO
#Possivelmente definir forms e views individuais para editar e adicionar, o conteúdo destas pode vir a ser grande demais para modals

#Regista um novo evento a ser promovido.

@transaction.atomic


#Remove um evento e retorna à pagina principal dos eventos
def remove_event(request, pk):
    event = Event.objects.get(id=pk)
    event.delete()
    return redirect('eventos')

def create_event(request):
    if request.method == 'POST':
        erros = []
        event = EventForm(request.POST, request.FILES)
        if event.is_valid():
            data = event.cleaned_data
            imageStore = EventImages()
            if data["date_initial"] > data["date_final"]:
                return redirect(request.META['HTTP_REFERER'])
            #import pdb; pdb.set_trace()
            if 'image1' in request.FILES or 'image2' in request.FILES or 'image3' in request.FILES:
                if 'image1' in request.FILES:
                    image = request.FILES['image1']
                    if(imageValidation(Image.open(image), image._size, erros)):
                        fs = FileSystemStorage()
                        fs.save(image.name, image)
                        imageStore.image1 = data['image1']
                if 'image2' in request.FILES:
                    image = request.FILES['image2']
                    if(imageValidation(Image.open(image), image._size, erros)):
                        fs = FileSystemStorage()
                        fs.save(image.name, image)
                        imageStore.image2 = data['image2']
                if 'image3' in request.FILES:
                    image = request.FILES['image3']
                    if(imageValidation(Image.open(image), image._size, erros)):
                        fs = FileSystemStorage()
                        fs.save(image.name, image)
                        imageStore.image3 = data['image3']
                if(len(erros) > 0):
                    return render(request, 'create_evento.html',{'erros':erros})
                else:
                    imageStore.save()
            else:
                return redirect(request.META['HTTP_REFERER'])
            tutors = data["listTutor"].split(";")
            event = Event(local=data["local"], name=data["name"], date_initial=data["date_initial"],
                          date_final=data["date_final"], about=data["about"], type=data["type"],
                          max_participants=data["max_participants"], creator=request.user,
                          latitude=data["latitude"], longitude=data["longitude"],images=imageStore)
            event.save()
            for i in range(len(tutors)):
                tutorData = TutorEvent(tutorName = tutors[i], event = event)
                tutorData.save()
            return redirect(create_success)
        else:
            for e in event.errors:
                erros.append(event.errors[e])
            return render(request, 'create_evento.html',{'erros':erros})
    else:
        if('Safari' in request.user_agent.browser.family):
            return render(request,'create_evento_safari.html')
        else:
            return render(request, 'create_evento.html')

def imageValidation(image, size, erros):
    MAX_FILESIZE = 5242880
    MAX_WIDTH = 10000
    MAX_HEIGHT = 10000
    MIN_WIDTH = 2
    MIN_HEIGHT = 2
    if(size > MAX_FILESIZE):
        erros.append('Por favor carregue imagens de tamanho inferior a 5MBs')
    if(image.size[0] > MAX_HEIGHT or image.size[1] > MAX_WIDTH):
        erros.append('A sua imagem não deve exceder as dimensões 10000x10000')
    if(image.size[0] < MIN_HEIGHT or image.size[1] < MIN_WIDTH):
        erros.append('A sua imagem tem de ser ser maior que 400x400')
    if(len(erros) > 0):
        return False
    else:
        return True

def create_success(request):
    return render(request, 'create_evento_success.html')

def manage_events(request):
    events = Event.objects.all()
    events_validated = []
    events_notvalidated = []
    for event in events:
        if event.validated:
            events_validated.append(event)
        else:
            events_notvalidated.append(event)
    return render(request, 'manage_events.html', {"events_notvalidated": events_notvalidated, "events_validated": events_validated})

def manage_events_view(request, pk):
    try:
        if request.method == 'POST':
            mail = MailForm(request.POST)
            if mail.is_valid():
                data = mail.cleaned_data
                event = Event.objects.get(id=pk)
                user = event.creator
                contents = {'email': user.email,'domain': request.META['HTTP_HOST'],'site_name': 'Malta e Companhia Website',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),'user': user, 'adminMail': data["emailEvent"],
                            'token': default_token_generator.make_token(user),'protocol': 'http', 'eventId':event.id}
                subject_template_name='validate_event_subject.txt'
                email_template_name='validate_event_email.html'
                subject = loader.render_to_string(subject_template_name, contents)
                subject = ''.join(subject.splitlines())
                email = loader.render_to_string(email_template_name, contents)
                send_mail(subject, email, settings.DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                infoMsg= "Email enviado."
                event_participations = EventParticipation.objects.filter(event_id=event.id)
                current_user = request.user
                event_participations_user = EventParticipation.objects.filter(event_id=event.id, user_id=current_user.id)
                user_ids_participating = event_participations.values("user_id")
                # participating_users = Utilizador.objects.filter(pk__in=user_ids_participating)
                now = timezone.now()
                date_initial = str(event.date_initial.date())
                date_final = str(event.date_final.date())
                time_initial = str(event.date_initial.time())
                time_final = str(event.date_final.time())
                types = EventType.objects.all()
                event_tutors = TutorEvent.objects.filter(event=pk)
                event_images = event.images
                event_creator = event.creator
                participating_users = event_participations.count()
                participating_max = event.max_participants

                if event_participations_user.count() != 0:
                    exists = "yes"
                else:
                    exists = "no"

                if event_participations.count() >= event.max_participants:
                    full = "yes"
                else:
                    full = "no"
                return render(request, 'manage_events_view.html', {"event": event, "exist": exists, "date_initial": date_initial, "time_initial": time_initial, "types": types, "current_user": current_user,
                                                            "event_tutors":event_tutors, "date_final": date_final, "time_final": time_final, "full": full, "event_creator": event_creator,
                                                            "event_images":event_images, "participating_users": participating_users, "participating_max": participating_max, "now": now,"infoMsg":infoMsg})

        else:
            event = Event.objects.get(id=pk)
            event_participations = EventParticipation.objects.filter(event_id=event.id)
            current_user = request.user
            event_participations_user = EventParticipation.objects.filter(event_id=event.id, user_id=current_user.id)
            user_ids_participating = event_participations.values("user_id")
            participating_users = Utilizador.objects.filter(pk__in=user_ids_participating)
            now = timezone.now()
            date_initial = str(event.date_initial.date())
            date_final = str(event.date_final.date())
            time_initial = str(event.date_initial.time())
            time_final = str(event.date_final.time())
            types = EventType.objects.all()
            event_tutors = TutorEvent.objects.filter(event=pk)
            event_images = event.images
            event_creator = event.creator
            if event_participations_user.count() != 0:
                exists = "yes"
            else:
                exists = "no"

            if event_participations.count() >= event.max_participants:
                full = "yes"
            else:
                full = "no"
            return render(request, 'manage_events_view.html', {"event": event, "exist": exists, "date_initial": date_initial, "time_initial": time_initial, "types": types, "current_user": current_user,
                                                        "event_tutors":event_tutors, "date_final": date_final, "time_final": time_final, "full": full, "event_creator": event_creator,
                                                        "event_images":event_images, "participating_users": participating_users, "now": now})
    except Event.DoesNotExist:
        return render(request, 'misc/index.html')

def validate_event(request, pk):
    try:
        event = Event.objects.get(id=pk)
        event.validated = True
        event.save()
        return redirect(manage_events);
    except Event.DoesNotExist:
        return render(request, 'misc/index.html')

def edit_event(request, pk):
    if request.method == 'POST':
        erros = []
        event = EventForm(request.POST, request.FILES)
        if event.is_valid():
            data = event.cleaned_data
            evento = Event.objects.get(id=pk)
            event_tutors = TutorEvent.objects.filter(event=pk)
            event_images = evento.images
            if(evento.creator != request.user):
                return render(request, 'misc/index.html')
            if 'image1' in request.FILES:
                image = request.FILES['image1']
                if(imageValidation(Image.open(image), image._size, erros)):
                    fs = FileSystemStorage()
                    fs.save(image.name, image)
                    event_images.image1 = data['image1']
            if 'image2' in request.FILES:
                image = request.FILES['image2']
                if(imageValidation(Image.open(image), image._size, erros)):
                    fs = FileSystemStorage()
                    fs.save(image.name, image)
                    event_images.image2 = data['image2']
            if 'image3' in request.FILES:
                image = request.FILES['image3']
                if(imageValidation(Image.open(image), image._size, erros)):
                    fs = FileSystemStorage()
                    fs.save(image.name, image)
                    event_images.image3 = data['image3']
            if(len(erros) > 0):
                context = get_event(request,pk)
                context['erros'] = erros
                return render(request, 'edit_evento.html', context)
            else:
                event_images.save()
            tutors = data["listTutor"].split(";")
            for i in range(len(tutors)):
                event_tutors[i].tutorName = tutors[i]
                event_tutors[i].save()
            evento.name=data["name"]
            evento.date_initial=data["date_initial"]
            evento.date_final=data["date_final"]
            evento.about=data["about"]
            evento.type=data["type"]
            evento.max_participants=data["max_participants"]
            evento.local = data["local"]
            evento.latitude=data["latitude"]
            evento.longitude=data["longitude"]
            evento.validated=False
            evento.save()
            return render(request, 'edit_success.html')
        else:
            for e in event.errors:
                erros.append(event.errors[e])
            context = get_event(request,pk)
            context['erros'] = erros
            return render(request, 'edit_evento.html', context)
    else:
        context = get_event(request,pk)
        if context == -1:
            return HttpResponse('<p>Permission Denied</p>')
        if context == -2:
            return HttpResponse('<p>Page not found</p>')
        return render(request, 'edit_evento.html', context)

def get_event(request,pk):
    try:
        event = Event.objects.get(id=pk)
        event_tutors = TutorEvent.objects.filter(event=pk)
        participating_max = event.max_participants
        event_images = event.images
        if(event.creator == request.user or request.user.is_staff):
            #event_participations_user = EventParticipation.objects.filter(event_id=event.id, user_id=current_user.id)
            #user_ids_participating = event_participations.values("user_id")
            di = str(event.date_initial.year)+"-"+str(event.date_initial.month)+"-"+str(event.date_initial.day)
            df = str(event.date_final.year)+"-"+str(event.date_final.month)+"-"+str(event.date_final.day)
            hi = str(event.date_initial.hour)+":"+str(event.date_initial.minute)
            hf = str(event.date_final.hour)+":"+str(event.date_final.minute)
            image1,image2,image3 = bool(event_images.image1),bool(event_images.image2),bool(event_images.image3)
            url1,url2,url3, = '','',''
            if(image1):
                url1 = "http://"+request.META['HTTP_HOST']+event_images.image1.url
            if(image2):
                url2 = "http://"+request.META['HTTP_HOST']+event_images.image2.url
            if(image3):
                url3 = "http://"+request.META['HTTP_HOST']+event_images.image3.url
            context = {"event":event, "images": event_images, "event_tutors": event_tutors,
                        "count_tutors": len(event_tutors), "date_inicial":di, "date_final":df,
                        "hour_inicial":hi,"hour_final":hf,"image1":image1,"image2":image2,"image3":image3,
                        "url1":url1,"url2":url2,"url3":url3}
            return context
        else:
            return -1
        #participating_users = Utilizador.objects.filter(pk__in=user_ids_participating)
        #now = timezone.now()
        #date_initial = str(event.date_initial.date()) + "T" + str(event.date_initial.time())
        #date_final = str(event.date_final.date()) + "T" + str(event.date_final.time())
        #types = EventType.objects.all()
        #if event_participations_user.count() != 0:
        #    exists = "yes"
        #else:
        #    exists = "no"

        #if event_participations.count() >= event.max_participants:
            #full = "yes"
        #else:
        #    full = "no"
        #context = {"event": event, "event_type": event_type, "exist": exists, "date_initial": date_initial, "types": types,
        #                "date_final": date_final, "full": full, "participating_users": participating_users, "now": now}

    except Event.DoesNotExist:
        return -2

#Ver detalhes do evento e processar pedidos sobre um evento
def event_view(request, pk):
    edited = False #Flag usada para mostrar alertas de edição bem sucedida na página de evento
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        user = request.user
        participation = EventParticipation(event=event, user=user)
        participation.save()
        return redirect(request.META['HTTP_REFERER'])
    else:
        if request.user.is_authenticated:
            if EventParticipation.objects.filter(user=request.user, event=event):
                registado = True
            else:
                registado = False
        else:
            registado = False

    try:
        event = Event.objects.get(id=pk)
        event_participations = EventParticipation.objects.filter(event_id=event.id)
        current_user = request.user
        event_participations_user = EventParticipation.objects.filter(event_id=event.id, user_id=current_user.id)
        user_ids_participating = event_participations.values("user_id")
        # participating_users = Utilizador.objects.filter(pk__in=user_ids_participating)
        now = timezone.now()
        date_initial = str(event.date_initial.date())
        date_final = str(event.date_final.date())
        time_initial = str(event.date_initial.time())
        time_final = str(event.date_final.time())
        types = EventType.objects.all()
        event_tutors = TutorEvent.objects.filter(event=pk)
        event_images = event.images
        event_creator = event.creator
        participating_users = event_participations.count()
        participating_max = event.max_participants

        if event_participations_user.count() != 0:
            exists = "yes"
        else:
            exists = "no"

        if event_participations.count() >= event.max_participants:
            full = "yes"
        else:
            full = "no"
        return render(request, 'perfilEvento.html', {"event": event, "exist": exists, "date_initial": date_initial, "time_initial": time_initial, "types": types, "current_user": current_user,
                                                    "event_tutors":event_tutors, "date_final": date_final, "time_final": time_final, "full": full, "event_creator": event_creator,
                                                    "event_images":event_images, "participating_users": participating_users,
                                                    "participating_max":participating_max, "registado":registado, "now": now})
    except Event.DoesNotExist:
        return render(request, 'misc/index.html')

#Recupera todos os eventos que tenha data e hora iniciais depois do momento atual.
def all_events_view(request):
    if request.method == 'POST':
        event = SearchForm(request.POST)
        if event.is_valid():
            data = event.cleaned_data
            events = Event.objects.all()
            nonvalidated_events = 0
            for event in events:
                if not event.validated:
                    nonvalidated_events += 1
            #import pdb; pdb.set_trace()
            now = timezone.now()
            if(data["searchtype"] == 'cat'):
                events = Event.objects.filter(type=data["categoria_search"])
            elif (data["searchtype"] == 'dat'):
                if data["dateini"] > data["dateend"]:
                    return redirect(request.META['HTTP_REFERER'])
                events = Event.objects.filter(date_initial__gte=data["dateini"]).filter(date_initial__lte=data["dateend"])
            elif (data["searchtype"] == 'loc'):
                events = Event.objects.filter(local=data["local_search"])
            events_past = []
            events_future = []
            for event in events:
                if event.validated:
                    if event.date_initial > now:
                        events_future.append(event)
                    else:
                        events_past.append(event)
            return render(request, 'eventos.html', {"events_past": events_past, "events_future": events_future, "nonvalidated_events": nonvalidated_events})
        else:
            HttpResponse(event.errors)
    else:
        events = Event.objects.all()
        now = timezone.now()
        events_past = []
        events_future = []
        nonvalidated_events = 0
        for event in events:
            if not event.validated:
                nonvalidated_events += 1
            elif event.date_initial > now:
                events_future.append(event)
            else:
                events_past.append(event)
        return render(request, 'eventos.html', {"events_past": events_past, "events_future": events_future, "nonvalidated_events": nonvalidated_events})
