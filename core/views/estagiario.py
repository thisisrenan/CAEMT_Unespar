from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from core.forms import EstagiarioForm, EstagiarioFormEdit
from core.models.users import Estagiario

from .core import is_supervisor

class EstagiarioCreate(CreateView):
    model = Estagiario
    form_class = EstagiarioForm
    template_name = 'estagiarioTemplate/estagiario_form.html'
    success_url = reverse_lazy('estagiarios')


@method_decorator(user_passes_test(is_supervisor, login_url='home'), name='dispatch')
class EstagiarioList(ListView):
    model = Estagiario
    template_name = 'estagiarioTemplate/estagiario_list.html'
    context_object_name = 'estagiarios'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Estagiario.objects.filter(username__icontains=query)
        return Estagiario.objects.all()


class EstagiarioEdit(UpdateView):
    model = Estagiario
    template_name = 'estagiarioTemplate/estagiario_form.html'
    form_class = EstagiarioFormEdit

class EstagiarioDelete(DeleteView):
    model = Estagiario
    context_object_name = 'estagiarios'
    template_name = 'estagiarioTemplate/estagiario_confirm_delete.html'
    success_url = reverse_lazy('estagiarios')


class EstagiarioEditProfile(UpdateView):
    model = Estagiario
    context_object_name = 'userProfile'
    fields = ['first_name', 'last_name','telefone','ano_letivo','biografia', 'outrasinformacoes','data_de_nascimento']
    template_name = 'perfiledit/perfilEdit.html'

    def get_object(self, queryset=None):
        return self.request.user.estagiario

    def get_success_url(self):
        return reverse_lazy('edit_profile')