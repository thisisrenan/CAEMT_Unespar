from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.views import View


from core.forms import EstagiarioForm, EstagiarioFormEdit
from core.models.users import Estagiario

from .core import is_supervisor

class EstagiarioCreate(CreateView):
    model = Estagiario
    form_class = EstagiarioForm
    template_name = 'estagiarioTemplate/estagiario_form.html'
    success_url = reverse_lazy('estagiarios')

    def form_valid(self, form):
        messages.success(self.request, "Estagiario criado com sucesso.")
        return super().form_valid(form)


    def form_invalid(self, form):
        errors = form.errors.as_text()
        messages.error(self.request, "Erro ao criar estagiário. Por favor, corrija os erros no formulário")
        return render(self.request, self.template_name, {'form': form})

class EstagiarioList(ListView):
    model = Estagiario
    template_name = 'estagiarioTemplate/estagiario_list.html'
    context_object_name = 'estagiarios'

    def get_queryset(self):
        query = self.request.GET.get('q')
        role_do_usuario = self.request.user.role

        estagiarios_ativos = Estagiario.objects.filter(is_active=True)

        if query:
            estagiarios_ativos = estagiarios_ativos.filter(username__icontains=query)

        if role_do_usuario == 'SUPERVISOR':
            estagiarios_desativados = Estagiario.objects.filter(is_active=False)
            estagiarios = estagiarios_ativos.union(estagiarios_desativados)
        else:
            estagiarios = estagiarios_ativos

        estagiarios = estagiarios.order_by('-is_active')

        return estagiarios

class EstagiarioEdit(UpdateView):
    model = Estagiario
    template_name = 'estagiarioTemplate/estagiario_form.html'
    form_class = EstagiarioFormEdit

    def form_valid(self, form):
        messages.success(self.request, "Estagiario atualizado com sucesso.")
        return super().form_valid(form)


class EstagiarioDelete(View):
    template_name = 'estagiarioTemplate/estagiario_confirm_delete.html'
    success_url = reverse_lazy('estagiarios')

    def get(self, request, pk):
        estagiario = get_object_or_404(Estagiario, pk=pk)
        return render(request, self.template_name, {'estagiario': estagiario})

    def post(self, request, pk):
        estagiario = get_object_or_404(Estagiario, pk=pk)
        estagiario.is_active = False
        estagiario.save()

        messages.success(request, "Estagiario deletado com sucesso.")
        return redirect(self.success_url)

class EstagiarioEditProfile(UpdateView):
    model = Estagiario
    context_object_name = 'userProfile'
    fields = ['first_name', 'last_name','telefone','ano_letivo','biografia', 'outrasinformacoes','data_de_nascimento']
    template_name = 'perfiledit/perfilEdit.html'

    def get_object(self, queryset=None):
        return self.request.user.estagiario

    def form_valid(self, form):
        messages.success(self.request, "Perfil atualizado com sucesso.")
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('edit_profile')

