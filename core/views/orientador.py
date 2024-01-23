

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from core.forms import OrientadorForm, OrientadorFormEdit
from core.models.users import Orientador

from .core import is_supervisor

class OrientadorCreate(CreateView):
    model = Orientador
    form_class = OrientadorForm
    template_name = 'orientadoreTemplate/orientador_form.html'
    success_url = reverse_lazy('orientadores')


class OrientadorList(ListView):
    model = Orientador
    template_name = 'orientadoreTemplate/orientador_list.html'
    context_object_name = 'orientadores'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Orientador.objects.filter(username__icontains=query)
        return Orientador.objects.all()

class OrientadorEdit(UpdateView):
    model = Orientador
    template_name = 'orientadoreTemplate/orientador_form.html'
    form_class = OrientadorFormEdit
    success_url = reverse_lazy('orientadores')

    def form_valid(self, form):
        messages.success(self.request, "Orientador atualizado com sucesso.")
        return super().form_valid(form)

class OrientadorDelete(DeleteView):
    model = Orientador
    success_url = reverse_lazy('orientadores')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Orientadores excluído com sucesso.")
        return super().delete(request, *args, **kwargs)



#edit Perfil

class OrientadorEditProfile(UpdateView):
    model = Orientador
    context_object_name = 'userProfile'
    fields =['first_name', 'last_name','telefone','biografia', 'outrasinformacoes','data_de_nascimento']
    template_name = 'perfiledit/perfilEdit.html'

    def get_object(self, queryset=None):
        return self.request.user.orientador

    def get_success_url(self):
        return reverse_lazy('edit_profile')

