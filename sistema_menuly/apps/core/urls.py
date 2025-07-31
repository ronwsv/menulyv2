"""
URLs do app core - páginas principais da plataforma.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurantes/', views.lista_restaurantes, name='lista_restaurantes'),
]
