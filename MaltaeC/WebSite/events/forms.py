#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
import datetime
from .models import EventType
#from mysite import settings
from django.contrib.admin import widgets

class EventForm(forms.Form):
    local = forms.CharField(max_length=300,error_messages={'required': 'Precisa de escolher um local'})
    image1 = forms.ImageField(required=False)
    image2 = forms.ImageField(required=False)
    image3 = forms.ImageField(required=False)
    name = forms.CharField(required=True, error_messages={'required': 'É obrigatório escolher um nome para o seu evento'})
    date_initial = forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M'],error_messages={'required': 'É obrigatório inserir uma data de ínicio'})
    date_final = forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M'],error_messages={'required': 'É obrigatório inserir uma data de fim'})
    about = forms.CharField(required=True, error_messages={'required': 'Tem de descrever o seu evento'})
    listTutor = forms.CharField(required=True, error_messages={'required': 'Precisa de definir um ou mais tutores'})
    max_participants = forms.IntegerField(required=True, error_messages={'required': 'É obrigatório definir o limite de participantes'})
    type = forms.CharField(required=True, error_messages={'required': 'Precisa de inserir um tipo de evento'})
    longitude = forms.FloatField()
    latitude = forms.FloatField()

class EventRegisterUser(forms.Form):
    event_id = forms.CharField()
    user_id = forms.CharField()

class EditEventForm(forms.Form):
    local = forms.CharField(max_length=300)
    name = forms.CharField(required=True)
    date_initial = forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M'])
    date_final = forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M'])
    about = forms.CharField()
    tutor = forms.CharField(max_length=100)
    max_participants = forms.IntegerField()
    type = forms.IntegerField()

class SearchForm(forms.Form):
    categoria_search = forms.CharField(required=False);
    local_search = forms.CharField(required=False);
    dateini = forms.DateField(required=False,input_formats=['%Y-%m-%d']);
    dateend = forms.DateField(required=False,input_formats=['%Y-%m-%d']);
    searchtype = forms.CharField(required=True);

class MailForm(forms.Form):
    emailEvent = forms.CharField(required=True, error_messages={'required': 'Não pode enviar um email em branco!'});
