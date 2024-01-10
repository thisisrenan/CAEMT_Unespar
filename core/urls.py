from django.urls import path
from django.urls import path, include

from . import views
from .views import OrientadorCreate, OrientadorList,OrientadorEdit,OrientadorDelete
urlpatterns = [
    path("", views.home, name="home"),

]
#URLS PERFIL
urlpatterns += [
    path('Orientador/novo', OrientadorCreate.as_view(), name='Create_Orientador'),
    path('Orientador/editar/<int:pk>', OrientadorEdit.as_view(), name='Edit_Orientador'),
    path('Orientador/Deletar/<int:pk>', OrientadorDelete.as_view(), name='Delete_Orientador'),

    path("Orientador", OrientadorList.as_view(), name="orientadores"),
    path("perfil/<str:username>", views.PerfilProfile, name='perfil'),
]