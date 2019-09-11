from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.conf import settings


class SettingsBackend(object):
    def authenticate(request, email=None, password=None):
        if BaseUser.objects.filter(email=email).exists():
            user = BaseUser.objects.filter(email=email).get()
            if user is not None:
                if user.check_password(password):
                    return user
            return None


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30, blank=True)
    phoneNumber = models.CharField(max_length=16, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    picUrl = models.CharField(max_length=500, default="media/userPics/user.png")
    type = models.CharField(max_length=16, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    reprovado = models.BooleanField(default=False)
    bio = models.TextField(default="")
    videoUrl = models.CharField(max_length=500, blank=True, default="")
    categorias = models.TextField(blank=True, default="")
    cidade = models.CharField(max_length=200, default="")
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_full_name(self):
        full_name = '%s %s' % (self.email, self.name)
        return full_name.strip()

    def get_short_name(self):
        return self.name


class PropostaRegisto(models.Model):
    texto = models.CharField(max_length=1000, blank=False, default='')
    imgUrl = models.CharField(max_length=500, blank=False, default=None)
    videoUrl = models.CharField(max_length=500, blank=True, default=None)


class ImageUser(models.Model):
    userEmail = models.EmailField()
    imgUrl = models.CharField(max_length=500, blank=False, default=None)


class Criativo(BaseUser):
    geolocation = models.CharField(max_length=500, default='')
    latitude = models.FloatField(null=True, blank=True, default=None)
    longitude = models.FloatField(null=True, blank=True, default=None)
    propostaRegisto = models.OneToOneField(PropostaRegisto, on_delete=models.CASCADE, primary_key=True, default=None)


    def __str__(self):
        return 'Criativo: ' + self.email


class Artesao(BaseUser):
    geolocation = models.CharField(max_length=500, default='')
    latitude = models.FloatField(null=True, blank=True, default=None)
    longitude = models.FloatField(null=True, blank=True, default=None)
    propostaRegisto = models.OneToOneField(PropostaRegisto, on_delete=models.CASCADE, primary_key=True, default=None)


    def __str__(self):
        return 'Artesao: ' + self.email


class Utilizador(BaseUser):
    adress = models.CharField(max_length=500)

    def __str__(self):
        return 'Utilizador: ' + self.email
