from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test, login_required

from core.models.users import Documentos, Participante
from .core import *
@method_decorator(user_passes_test(is_login, login_url='/ERRO'), name='dispatch')
class DocumentosCreate(CreateView):
    model = Documentos
    fields = ['titulo', 'descricao', 'arquivo']
    template_name = 'documentosTemplate/documentos_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participante_id = self.kwargs.get('participante_id')
        participante = get_object_or_404(Participante, id=participante_id)
        context['participante'] = participante
        return context

    def form_valid(self, form):
        participante_id = self.kwargs['participante_id']
        participante = Participante.objects.get(id=participante_id)
        form.instance.pertence = participante
        form.instance.criado_por = self.request.user
        messages.success(self.request, "Documento Adicionado com sucesso.")
        return super().form_valid(form)


@method_decorator(user_passes_test(is_login, login_url='/ERRO'), name='dispatch')
class DocumentosList(ListView):
    model = Documentos
    template_name = 'documentosTemplate/documentos_list.html'
    context_object_name = 'documentos'

    def get_queryset(self):
        participante_id = self.kwargs['participante_id']
        participante = get_object_or_404(Participante, id=participante_id)
        return participante.documentos_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participante_id = self.kwargs['participante_id']
        participante = get_object_or_404(Participante, id=participante_id)
        context['participante_id'] = participante_id
        context['participante_nome'] = participante.username

        return context

@method_decorator(user_passes_test(is_login, login_url='/ERRO'), name='dispatch')
class DocumentosDelete(DeleteView):
    model = Documentos
    context_object_name = 'documento'
    template_name = 'documentosTemplate/documento_confirm_delete.html'

    def get_success_url(self):
        participante_id = self.object.pertence.id

        success_url = reverse_lazy('List_Documetos', kwargs={'participante_id': participante_id})
        return success_url

    def form_valid(self, form):
        messages.success(self.request, "Documento excluído com sucesso.")
        return super().form_valid(form)