# coding=utf-8
from django.db import models
from WebSite.utilizadores.models import BaseUser
from django.db.models.signals import pre_save
from django.dispatch import receiver

#TODO
#Possibilidade de mais tutores

#EventType representa um categoria de evento.
class EventType(models.Model):
    event_name = models.CharField(max_length=100, blank=False)

#Um evento são açõe promovidas pela Malta&Companhia para estimular o contato entre pessoas interessadas no artesanato ou criação de
#produtos com outros métodos e os profissionais deste ofício.

class EventImages(models.Model):
    image1 = models.ImageField(upload_to="events", blank=True, height_field="height_field1", width_field="width_field1")
    image2 = models.ImageField(upload_to="events", blank=True, height_field="height_field2", width_field="width_field2")
    image3 = models.ImageField(upload_to="events", blank=True, height_field="height_field3", width_field="width_field3")
    height_field1 = models.IntegerField(default=200)
    width_field1 = models.IntegerField(default=300)
    height_field2 = models.IntegerField(default=200)
    width_field2 = models.IntegerField(default=300)
    height_field3= models.IntegerField(default=200)
    width_field3 = models.IntegerField(default=300)

class Event(models.Model):
    local = models.TextField()
    name = models.TextField()
    date_initial = models.DateTimeField(auto_now=False, auto_now_add=False)
    date_final = models.DateTimeField(auto_now=False, auto_now_add=False)
    about = models.TextField()
    tutor = models.TextField()
    max_participants = models.IntegerField()
    images = models.ForeignKey(EventImages, on_delete=models.CASCADE)
    #image = models.ImageField(upload_to="events", blank=True, height_field="height_field", width_field="width_field")
    height_field = models.IntegerField(default=200)
    width_field = models.IntegerField(default=300)
    type = models.TextField()
    #type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    validated = models.BooleanField(default=False)
    latitude = models.FloatField(default=0);
    longitude = models.FloatField(default=0);
    creator = models.ForeignKey(BaseUser, on_delete=models.CASCADE)

class TutorEvent(models.Model):
    tutorName = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

#Representa a praticipação de um usuario da plataforma em um evento promovido.

class EventParticipation(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
