"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main_app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('film', FilmApiView.as_view()),
    path('producer', ProducerApiView.as_view()),
    path('secret', SecretApiView.as_view()),
    path('registr', RegistrationApiView.as_view()),
    path('auth', AuthApiView.as_view()),
    path('cabinet', CabinetApiView.as_view()),
    path('cocktail', CocktailApiView.as_view()),
    path('filmget', FilmgetApiView.as_view()),
    path('filmfav', FavfilmApiView.as_view()),
    path('filmsearch', FilmSearchApiView.as_view()),
    path('filmsort',BookOrderApiView.as_view())
]
