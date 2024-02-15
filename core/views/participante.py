from datetime import datetime, time, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect


from django.views import View

from core.forms import ParticipanteForm, EnderecoForm, ResponsavelForm
from core.models.users import Participante, Endereco, Responsavel, agenda

from .core import *




@method_decorator(user_passes_test(is_supervisor_orientador, login_url='/ERRO'), name='dispatch')
class ParticipanteCreate(CreateView):
    model = Participante
    form_class = ParticipanteForm
    context_object_name = 'participantes'
    template_name = 'participanteTemplate/participante_form.html'
    success_url = reverse_lazy('participantes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', ParticipanteForm)
        context['responsavel_form'] = kwargs.get('responsavel_form', ResponsavelForm(prefix='responsavel'))
        return context

    def form_valid(self, form):
        responsavel_form = ResponsavelForm(self.request.POST, prefix='responsavel')
        for field_name, field_value in form.cleaned_data.items():
            item = form.cleaned_data[field_name]
            if field_name not in ['serie', 'escola', 'telefone']:
                if not item:
                    messages.warning(self.request, "O Campo'" + field_name + "'é obrigatorio")
                    return self.render_to_response(self.get_context_data(form=form, responsavel_form=responsavel_form))

        nome = form.cleaned_data['nome']
        sobrenome = form.cleaned_data['sobrenome']
        data_nascimento = form.cleaned_data['data_de_nascimento']
        username = f"{nome.replace(' ', '-')}-{sobrenome.replace(' ', '-')}"


        participante = Participante.objects.filter(username=username)
        if participante:
            messages.error(self.request, "Usuário já existe.")
            return self.render_to_response(self.get_context_data(form=form, responsavel_form=responsavel_form))

        form.instance.username = username


        today = datetime.today()
        age = today.year - data_nascimento.year - ((today.month, today.day) < (data_nascimento.month, data_nascimento.day))
        if age < 18:
            for field_name, field_value in responsavel_form.data.items():

                if field_name not in ['serie', 'escola']:
                    if not field_value:
                        messages.warning(self.request, f"Os dados do responsável são obrigatórios")
                        return self.render_to_response(self.get_context_data(form=form, responsavel_form=responsavel_form))


            if responsavel_form.is_valid():
                participante = form.save()
                nome_responsavel = responsavel_form.cleaned_data['nome']
                sobrenome_responsavel = responsavel_form.cleaned_data['sobrenome']
                telefone_responsavel = responsavel_form.cleaned_data['telefone']
                email_responsavel = responsavel_form.cleaned_data['email']

                responsavel = Responsavel.objects.create(
                    nome=nome_responsavel,
                    sobrenome=sobrenome_responsavel,
                    telefone=telefone_responsavel,
                    email=email_responsavel,
                    participante=participante
                )

            else:
                for field, errors in responsavel_form.errors.items():
                    for error in errors:
                        messages.warning(self.request, f"Erro no campo '{field}': {error}")
                return self.render_to_response(self.get_context_data(form=form, responsavel_form=responsavel_form))

            messages.success(self.request, "Responsável Criado com sucesso.")
        else:
            participante = form.save()

        response = super().form_valid(form)
        messages.success(self.request, "Participante Criado com sucesso.")
        return redirect('Create_Endereco', pk=self.object.id)

@method_decorator(user_passes_test(is_supervisor_orientador, login_url='/ERRO'), name='dispatch')
class ParticipanteList(ListView):
    model = Participante
    template_name = 'participanteTemplate/participante_list.html'
    context_object_name = 'participantes'
    paginate_by = 10

    def get_queryset(self):

        query = self.request.GET.get('q')
        user = self.request.user
        if user.role == 'ESTAGIARIO':
            if query:
                return Participante.objects.filter(estagiarios=user.estagiario, nome__icontains=query,is_active=True)
            return Participante.objects.filter(estagiarios=user.estagiario,is_active=True)
        else:
            if user.role == 'ORIENTADOR':
                if query:
                    return Participante.objects.filter(nome__icontains=query,is_active=True).order_by(F('date_joined').desc(), '-is_active')
                return Participante.objects.filter(is_active=True).order_by(F('date_joined').desc(), '-is_active')
            else:
                if query:
                    return Participante.objects.filter(nome__icontains=query).order_by(F('date_joined').desc(), '-is_active')
                return Participante.objects.all().order_by(F('date_joined').desc(), '-is_active')


@method_decorator(user_passes_test(is_supervisor_orientador, login_url='/ERRO'), name='dispatch')
class ParticipanteEdit(UpdateView):
    model = Participante
    form_class = ParticipanteForm
    context_object_name = 'participantes'
    template_name = 'participanteTemplate/participante_form_edit.html'

    def form_valid(self, form):
        messages.success(self.request, "Participante atualizado com sucesso.")
        return super().form_valid(form)


@method_decorator(user_passes_test(is_supervisor_orientador, login_url='/ERRO'), name='dispatch')
class ResponsalveEdit(UpdateView):
    model = Responsavel
    form_class = ResponsavelForm
    context_object_name = 'responsavel'
    template_name = 'participanteTemplate/responsavel_form_edit.html'
    def form_valid(self, form):
        messages.success(self.request, "responsavel atualizado com sucesso.")
        return super().form_valid(form)


@method_decorator(user_passes_test(is_supervisor_orientador, login_url='/ERRO'), name='dispatch')
class ParticipanterDelete(View):
    template_name = 'participanteTemplate/participante_confirm_delete.html'
    success_url = reverse_lazy('participantes')

    def get(self, request, pk):
        participante = get_object_or_404(Participante, pk=pk)
        return render(request, self.template_name, {'participante': participante})

    def post(self, request, pk):
        participante = get_object_or_404(Participante, pk=pk)
        try:
            agendaParticipante = agenda.objects.get(participante=participante)
        except ObjectDoesNotExist:
            agendaParticipante = None

        if agendaParticipante:
            agendaParticipante.delete()
        participante.is_active = False
        participante.save()

        messages.success(request, "Participante deletado com sucesso.")
        return redirect(self.success_url)


@method_decorator(user_passes_test(is_supervisor_orientador, login_url='/ERRO'), name='dispatch')
class EnderecoCreate(CreateView):
    model = Endereco
    form_class = EnderecoForm
    context_object_name = 'endereco'
    template_name = 'enderecoTemplate/endereco_form.html'
    success_url = reverse_lazy('participantes')

    def form_valid(self, form):
        participante_id = self.kwargs['pk']
        participante = Participante.objects.get(pk=participante_id)
        form.instance.participante = participante
        messages.success(self.request, "Endereço cadastrato com sucesso.")
        response = super().form_valid(form)

        return redirect(reverse('agendaEdit', args=['segunda-feira', participante.username]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participante_id = self.kwargs['pk']
        participante = get_object_or_404(Participante, id=participante_id)
        context['participante'] = participante
        return context

    def get_success_url(self):
        return reverse_lazy('participantes')  # Substitua 'sua_pagina_desejada' pela URL desejada


@method_decorator(user_passes_test(is_supervisor_orientador, login_url='/ERRO'), name='dispatch')
class EnderecoEdit(UpdateView):
    model = Endereco
    form_class = EnderecoForm
    context_object_name = 'endereco'
    template_name = 'enderecoTemplate/endereco_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Endereço atualizado com sucesso.")
        return super().form_valid(form)


@user_passes_test(is_supervisor, login_url='/ERRO')
def reativarParticipante(request, pk):
    user = get_object_or_404(Participante, id=pk)
    user.is_active = True
    user.save()
    messages.success(request, "Participante ativado com sucesso.")

    return redirect('participantes')

@login_required
def PerfilParticipante(request, username):
    participante = get_object_or_404(Participante,username=username)
    context = {
        "participante": participante
    }
    return render(request, 'participanteTemplate/perfilparticipante.html', context)