from django.db import models
from WebSite.utilizadores.models import BaseUser

class EmailsBanidos(models.Model):
	email = models.EmailField(max_length=64,unique=True)

	def __str__(self):
		return '' + self.email


class Entrevista(models.Model):
	userID = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
	conteudoEntrevista = models.TextField()

	def __str__(self):
		return 'Entrevista' + str(self.userID.id)

class CarouselIMGs(models.Model):
	img1 = models.CharField(max_length=500, blank=False, default="media/index_carousel/1.png")
	img2 = models.CharField(max_length=500, blank=False, default="media/index_carousel/2.png")
	img3 = models.CharField(max_length=500, blank=False, default="media/index_carousel/3.png")
	img4 = models.CharField(max_length=500, blank=False, default="media/index_carousel/4.png")
	img5 = models.CharField(max_length=500, blank=False, default="media/index_carousel/5.png")

	def __str__(self):
		return 'CarouselIMGs: ' + str(self.img1)