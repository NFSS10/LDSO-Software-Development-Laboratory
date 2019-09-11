import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MaltaCProject.settings")
import django
django.setup()

#########################################################################
#Inserir dados de teste na BD
#Para inserir a info. usar comando: python DBinsertTestData.py

from passlib.hash import pbkdf2_sha256
from WebSite.utilizadores.models import Utilizador


#--------- Dados ---------#

#Utilizadores:
enc_pwd = pbkdf2_sha256.encrypt("pass", rounds = 6000, salt_size = 32)
user = Utilizador(name = "Nuno", email = "a@b.com",
			  password = enc_pwd, phoneNumber = "911111",adress = "Rua coiso e tal")
user.save()
user = Utilizador(name = "Antonio", email = "antonio@email.com",
			  password = enc_pwd, phoneNumber = "911111",adress = "Rua coiso e tal")
user.save()
user = Utilizador(name = "Emanuel", email = "ema@email.com",
			  password = enc_pwd, phoneNumber = "911111",adress = "Rua coiso e tal")
user.save()
user = Utilizador(name = "ZeNaifas", email = "ze@email.com",
			  password = enc_pwd, phoneNumber = "911111",adress = "Rua coiso e tal")
user.save()
