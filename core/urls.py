from django.urls import path
from django.urls import path, include

from . import views
from .views import *
urlpatterns = [
    path("", views.home, name="home"),

]
#URLS PERFIL
urlpatterns += [
    path("perfil/<str:username>", views.PerfilProfile, name='perfil'),
]

#URLS SUPERVISOR
urlpatterns += [
    path('Supervisor/novo', SupervisorCreate.as_view(), name='Create_Supervisor'),
    path('Supervisor/editar/<int:pk>', SupervisorEdit.as_view(), name='Edit_Supervisor'),
    path('Supervisor/Deletar/<int:pk>', SupervisorDelete.as_view(), name='Delete_Supervisor'),
    path("Supervisor", SupervisorList.as_view(), name="supervisores"),
]

#URLS ORIENTADOR
urlpatterns += [
    path('Orientador/novo', OrientadorCreate.as_view(), name='Create_Orientador'),
    path('Orientador/editar/<int:pk>', OrientadorEdit.as_view(), name='Edit_Orientador'),
    path('Orientador/Deletar/<int:pk>', OrientadorDelete.as_view(), name='Delete_Orientador'),
    path("Orientador", OrientadorList.as_view(), name="orientadores"),
]

#URLS ESTAGIARIO
urlpatterns += [
    path('Estagiario/novo', EstagiarioCreate.as_view(), name='Create_Estagiario'),
    path('Estagiario/editar/<int:pk>', EstagiarioEdit.as_view(), name='Edit_Estagiario'),
    path('Estagiario/Deletar/<int:pk>', EstagiarioDelete.as_view(), name='Delete_Estagiario'),
    path("Estagiario", EstagiarioList.as_view(), name="estagiarios"),
]

#URLS Participante
urlpatterns += [
    path('Participante/novo', ParticipanteCreate.as_view(), name='Create_Participante'),
    path('Participante/editar/<int:pk>', ParticipanteEdit.as_view(), name='Edit_Participante'),
    path('Participante/Deletar/<int:pk>', ParticipanterDelete.as_view(), name='Delete_Participante'),
    path("Participante", ParticipanteList.as_view(), name="participantes"),
]

#URLS endereco
urlpatterns += [
    path('Endereco/novo/<int:pk>', EnderecoCreate.as_view(), name='Create_Endereco'),
    path('Endereco/editar/<int:pk>', EnderecoEdit.as_view(), name='Edit_Endereco'),
]