from django.db import models
from django.conf import settings


class PostImage(models.Model):
    #    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="image")


#    def __unicode__(self):
#        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100, default='')
    text = models.TextField()
    data = models.DateField(auto_now=False, auto_now_add=True)
    image1 = models.ImageField(upload_to="blog/", blank=True)
    image2 = models.ImageField(upload_to="blog/", blank=True)
    image3 = models.ImageField(upload_to="blog/", blank=True)
    image4 = models.ImageField(upload_to="blog/", blank=True)
