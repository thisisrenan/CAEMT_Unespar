import secrets

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.contrib.auth.views import PasswordChangeView

from core.forms import inputImage
from core.models import User
from core.models.users import UserActivity, Atendimentos, agenda, Participante, Estagiario, Orientador


def is_supervisor(user):
    return user.is_authenticated and user.role == 'SUPERVISOR'

def is_orientador(user):
    return user.is_authenticated and user.role == 'ORIENTADOR'

def is_estagiario(user):
    return user.is_authenticated and user.role == 'ESTAGIARIO'


def get_logged_in_users():
    users_activity = UserActivity.objects.all().order_by('-last_activity')

    return users_activity

def index(request):

    return render(request, 'registration/login.html', {})

@login_required
def homeEstagiario(request):
    user = request.user
    data_atual = timezone.now().date()
    datas_proximos_7_dias = [data_atual + timezone.timedelta(days=i) for i in range(7)]
    agendamentos = agenda.objects.filter(estagiario=user,
                                         dia_da_semana__in=[data.weekday() for data in datas_proximos_7_dias])
    #fazer os atendimentos atualizar, ele busca os proximos 7 dias
    data = []
    for n in agendamentos:
        # Calcula a data usando o dia da semana e a data atual
        dia_atual = data_atual.weekday()
        dias_para_frente = (n.dia_da_semana - dia_atual + 7) % 7
        data_calculada = data_atual + timezone.timedelta(days=dias_para_frente)

        data.append(f"{data_calculada.strftime('%d/%m/%Y')} - {agenda.SEMANA_CHOICES[n.dia_da_semana][1]}")
    ids_atendimentos_para_excluir = []
    for atendimento in Atendimentos.objects.filter(estagiario=user, ocorreu=False):
        dia_semana_atendimento = atendimento.data_atendimento.weekday()

        if dia_semana_atendimento not in [agendamento.dia_da_semana for agendamento in agendamentos] or \
                atendimento.data_atendimento.time() not in [agendamento.horario for agendamento in agendamentos]:
            ids_atendimentos_para_excluir.append(atendimento.id)
    Atendimentos.objects.filter(id__in=ids_atendimentos_para_excluir).delete()
    for agendamento in agendamentos:
        data_calculada = data_atual + timezone.timedelta(
            days=(agendamento.dia_da_semana - data_atual.weekday() + 7) % 7)

        atendimento_existente = Atendimentos.objects.filter(
            participante=agendamento.participante,
            data_atendimento=timezone.make_aware(timezone.datetime.combine(data_calculada, agendamento.horario)),
            estagiario__in=agendamento.estagiario.all()
        ).first()

        if not atendimento_existente:
            novo_atendimento = Atendimentos.objects.create(
                participante=agendamento.participante,
                data_atendimento=timezone.make_aware(timezone.datetime.combine(data_calculada, agendamento.horario))
            )
            for estagiario in agendamento.estagiario.all():
                novo_atendimento.estagiario.add(estagiario)
            novo_atendimento.save()


    participantes = []

    for agendamento in agenda.objects.filter(estagiario=user):
        participantes.append(agendamento.participante)

    atendimentos_previstos = Atendimentos.objects.filter(ocorreu=False, estagiario=user).order_by('data_atendimento')
    atendimentos_ocorridos = Atendimentos.objects.filter(ocorreu=True, estagiario=user).order_by('data_atendimento')

    context = {
        "data_hj": data_atual,
        "atendimentos_previstos":atendimentos_previstos,
        "atendimentos_ocorridos":atendimentos_ocorridos,
        "participantes": participantes
    }
    print(participantes)
    return render(request, "indexEstagiario.html", context)


@login_required
def homeOrientador(request):
    user = request.user
    estagiarios = Estagiario.objects.filter(orientador_responsavel=user.id)


    participantes = []
    atendimentos_ocorridos = []
    for estagiario in estagiarios:
        atendimentos = Atendimentos.objects.filter(estagiario=estagiario, ocorreu=True)
        for atendimento in atendimentos:
            atendimentos_ocorridos.append(atendimento)

        agendas = agenda.objects.filter(estagiario=estagiario)
        for agendas in agendas:
            participantes.append(agendas.participante)

    users = get_logged_in_users()
    context = {
        "estagiarios": estagiarios,
        "participantes": participantes,
        "atendimentos_ocorridos": atendimentos_ocorridos
    }
    print(participantes)
    return render(request, "indexOrientador.html", context)

def homeSupervisor(request):
    user = request.user
    estagiarios = Estagiario.objects.filter(is_active=True)
    orientadores = Orientador.objects.filter(is_active=True)
    participantes = Participante.objects.filter(is_active=True)
    atendimentos_ocorridos = Atendimentos.objects.filter(ocorreu=True)
    usuarios_logados = get_logged_in_users()
    users = get_logged_in_users()
    context = {
        "logados": usuarios_logados,
        "estagiarios": estagiarios,
        "participantes": participantes,
        "orientadores": orientadores,
        "atendimentos_ocorridos": atendimentos_ocorridos
    }
    print(participantes)
    return render(request, "indexSupervisor.html", context)

@login_required
def PerfilProfile(request, username):
    user = get_object_or_404(User,username=username)
    context = {
        "userProfile": user
    }
    return render(request, 'perfil/perfil.html', context)

#edit perfil
def reativarUsuario(request, pk):
    user = get_object_or_404(User, id=pk)
    user.is_active = True
    user.save()
    messages.success(request, f"{user.role.capitalize()} ativado com sucesso.")


    referer = request.META.get('HTTP_REFERER')

    if referer:
        return HttpResponseRedirect(referer)
    else:
        return HttpResponseRedirect(reverse('home'))


def redefinirSenha(request,pk):
    user = get_object_or_404(User, id=pk)
    senha = secrets.token_urlsafe(6)
    user.password = make_password(senha)
    user.save()
    messages.success(request,
                  f"Senha Redefinida com Sucesso.<br> Email do usuário: {user.email} <br> Senha do usuário: {senha}", )

    referer = request.META.get('HTTP_REFERER')

    if referer:
        return HttpResponseRedirect(referer)
    else:
        return HttpResponseRedirect(reverse('home'))

class SupervisorEditImage(UpdateView):
    model = User
    context_object_name = 'userProfile'
    form_class = inputImage
    template_name = 'perfiledit/perfilEdit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Imagem atualizada com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('edit_photo')


class SupervisorChangePasswordView(PasswordChangeView):
    template_name = 'perfiledit/changePassword.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('edit_profile')




