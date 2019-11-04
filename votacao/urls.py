from django.contrib import admin
from django.urls import path
from .views import home, mostra_chapa, votar, secret_code, voto_branco

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('chapa/', mostra_chapa, name='chapa'),
    path('votado/', votar, name='votado'),
    path('branco/', voto_branco, name='branco'),
    path('secret_code/', secret_code, name='secret'),
]