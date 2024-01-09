from django.urls import path
from django.urls import path, include

from . import views
from .views import OrientadorCreate, OrientadorList
urlpatterns = [
    path("", views.home, name="home"),

]
#URLS PERFIL
urlpatterns += [
    path('Orientador/novo', OrientadorCreate.as_view(), name='Create_Orientador'),
    path("Orientador", OrientadorList.as_view(), name="orientadores"),
    path("perfil/<str:username>", views.PerfilProfile, name='perfil'),
]