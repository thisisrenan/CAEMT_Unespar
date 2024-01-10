from django.urls import path
from django.urls import path, include

from . import views
from .views import *
urlpatterns = [
    path("", views.home, name="home"),

]
#URLS PERFIL
urlpatterns += [
    path('Orientador/novo', OrientadorCreate.as_view(), name='Create_Orientador'),
    path('Orientador/editar/<int:pk>', OrientadorEdit.as_view(), name='Edit_Orientador'),
    path('Orientador/Deletar/<int:pk>', OrientadorDelete.as_view(), name='Delete_Orientador'),
    path("Orientador", OrientadorList.as_view(), name="orientadores"),

    path('Estagiario/novo', EstagiarioCreate.as_view(), name='Create_Estagiario'),
    path('Estagiario/editar/<int:pk>', EstagiarioEdit.as_view(), name='Edit_Estagiario'),
    path('Estagiario/Deletar/<int:pk>', EstagiarioDelete.as_view(), name='Delete_Estagiario'),
    path("Estagiario", EstagiarioList.as_view(), name="estagiarios"),

    path("perfil/<str:username>", views.PerfilProfile, name='perfil'),
]