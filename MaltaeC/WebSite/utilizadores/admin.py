from django.contrib import admin
from .models import BaseUser, Criativo, Artesao, Utilizador, BaseUser

admin.site.register(BaseUser)
admin.site.register(Criativo)
admin.site.register(Artesao)
admin.site.register(Utilizador)
