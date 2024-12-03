from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class Film(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    producer = models.ForeignKey('Producer', on_delete=models.CASCADE, null=True, blank=True)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, null=True, blank=True)
    languages = models.ManyToManyField('Language')
    awards = models.ManyToManyField('Awards')

    def __str__(self):
        return self.name

class Producer(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField()
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Awards(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if email is None:
            raise ValueError('Email is required!')
        email = self.normalize_email(email)
        # self.normalize_email -> Встроенный метод в Джанго, для приведения имейла в порядок
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # set_password -> Сохраняет хэш пароля
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    fav_films = models.ManyToManyField('Film', blank = True)
    # auto_now_add -> Автоматически добавляет текущую при создании объекта

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()