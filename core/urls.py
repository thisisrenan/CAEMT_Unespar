
from django.urls import path, include
from django.conf.urls.static import static

from CAEMTUnespar import settings
from . import views
from .views.agenda import *
from .views.estagiario import *
from .views.orientador import *
from .views.participante import *
from .views.supervisor import *
from .views.documentos import *
from .views.core import *


def edit_profile_view(request):
    # Determine a role do usuário
    user_role = request.user.role

    # Escolha a visualização com base na role do usuário
    if user_role == User.Role.ORIENTADOR:
        view_class = OrientadorEditProfile  # Substitua pelo nome da sua view para Orientador
    elif user_role == User.Role.SUPERVISOR:
        view_class = SupervisorEditProfile
    else:
        view_class = EstagiarioEditProfile
    view_instance = view_class.as_view()

    return view_instance(request)

urlpatterns = [
    path("", home, name="home"),
    path("agenda", rediAgenda, name='agendas'),
    path("agenda/<str:semana>", agendaHome, name='agenda'),
    path('agenda/criar/<str:semana>', criar_agenda, name='create_agenda'),
    path('agenda/deletar/<int:pk>', deletar_agenda, name='deletar_agenda'),

]

#URLS PERFIL
urlpatterns += [
    path('perfil/editarPerfil', edit_profile_view, name='edit_profile'),
    path('perfil/editarFoto', SupervisorEditImage.as_view(), name='edit_photo'),
    path('perfil/editarConta', SupervisorChangePasswordView.as_view(), name='edit_account'),
    path("perfil/<str:username>", PerfilProfile, name='perfil'),
]

#URLS CORE
urlpatterns += [
    path('Reativar/<int:pk>', reativarUsuario, name='reativar_user'),
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

#URLS PARTICIPANTE
urlpatterns += [
    path('Participante/novo', ParticipanteCreate.as_view(), name='Create_Participante'),
    path('Participante/editar/<int:pk>', ParticipanteEdit.as_view(), name='Edit_Participante'),
    path('Participante/Deletar/<int:pk>', ParticipanterDelete.as_view(), name='Delete_Participante'),
    path("Participante", ParticipanteList.as_view(), name="participantes"),
    path('ReativarParticipante/<int:pk>', reativarParticipante, name='reativar_participante'),
]

#URLS ENDERECO
urlpatterns += [
    path('Endereco/novo/<int:pk>', EnderecoCreate.as_view(), name='Create_Endereco'),
    path('Endereco/editar/<int:pk>', EnderecoEdit.as_view(), name='Edit_Endereco'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urls DOCUMENTOS
urlpatterns += [
    path('Documentos/novo/<int:participante_id>', DocumentosCreate.as_view(), name='Create_Documetos'),
    path('Documentos/<int:participante_id>', DocumentosList.as_view(), name='List_Documetos'),
    path('Documentos/<int:participante_id>/<str:participante_nome>', DocumentosList.as_view(), name='List_Documetos'),
    path('Documentos/Deletar/<int:pk>', DocumentosDelete.as_view(), name='Delete_Documetos'),

]