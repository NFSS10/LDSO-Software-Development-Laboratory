from django.db import models


class Tool(models.Model):
	userId = models.IntegerField()
	name = models.CharField(max_length=255)
	description = models.TextField()
	price = models.FloatField()
	imageUrl = models.TextField()