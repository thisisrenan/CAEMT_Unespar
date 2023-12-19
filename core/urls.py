from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),

]
#URLS PERFIL
urlpatterns += [
    path("perfil/<str:username>", views.PerfilProfile, name='perfil'),
]