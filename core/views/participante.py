from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect


from django.views import View

from core.forms import ParticipanteForm, EnderecoForm
from core.models.users import Participante, Endereco

from .core import is_supervisor

class ParticipanteCreate(CreateView):
    model = Participante
    form_class = ParticipanteForm
    context_object_name = 'participantes'
    template_name = 'participanteTemplate/participante_form.html'
    success_url = reverse_lazy('participantes')

    def form_valid(self, form):
        nome = form.cleaned_data['nome']
        sobrenome = form.cleaned_data['sobrenome']
        username = f"{nome.replace(' ', '').capitalize()}_{sobrenome.replace(' ', '').capitalize()}"
        if Participante.objects.filter(username=username).exists():
            messages.error(self.request, f"Erro ao criar o participante. O Participante '{username}' já está em uso.")
            return self.render_to_response(self.get_context_data(form=form))

        form.instance.username = username

        response = super().form_valid(form)
        messages.success(self.request, "Participante Criado com sucesso.")
        return redirect('Create_Endereco', pk=self.object.id)


class ParticipanteList(ListView):
    model = Participante
    template_name = 'participanteTemplate/participante_list.html'
    context_object_name = 'participantes'

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
                    return Participante.objects.filter(nome__icontains=query,is_active=True).order_by('-is_active')
                return Participante.objects.filter(is_active=True).order_by('-is_active')
            else:
                if query:
                    return Participante.objects.filter(nome__icontains=query).order_by('-is_active')
                return Participante.objects.all().order_by('-is_active')

class ParticipanteEdit(UpdateView):
    model = Participante
    form_class = ParticipanteForm
    context_object_name = 'participantes'
    template_name = 'participanteTemplate/participante_form_edit.html'

    def form_valid(self, form):
        messages.success(self.request, "Participante atualizado com sucesso.")
        return super().form_valid(form)


class ParticipanterDelete(View):
    template_name = 'participanteTemplate/participante_confirm_delete.html'
    success_url = reverse_lazy('participantes')

    def get(self, request, pk):
        participante = get_object_or_404(Participante, pk=pk)
        return render(request, self.template_name, {'participante': participante})

    def post(self, request, pk):
        participante = get_object_or_404(Participante, pk=pk)
        participante.is_active = False
        participante.save()

        messages.success(request, "Participante deletado com sucesso.")
        return redirect(self.success_url)

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
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('participantes')  # Substitua 'sua_pagina_desejada' pela URL desejada


class EnderecoEdit(UpdateView):
    model = Endereco
    form_class = EnderecoForm
    context_object_name = 'endereco'
    template_name = 'enderecoTemplate/endereco_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Endereço atualizado com sucesso.")
        return super().form_valid(form)


def reativarParticipante(request, pk):
    user = get_object_or_404(Participante, id=pk)
    user.is_active = True
    user.save()
    messages.success(request, "Participante ativado com sucesso.")

    return redirect('participantes')
