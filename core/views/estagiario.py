import secrets

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password

from django.views import View


from core.forms import EstagiarioForm, EstagiarioFormEdit
from core.models.users import Estagiario, User

from .core import *

@method_decorator(user_passes_test(is_supervisor_orientador, login_url='/ERRO'), name='dispatch')
class EstagiarioCreate(CreateView):
    model = Estagiario
    form_class = EstagiarioForm
    template_name = 'estagiarioTemplate/estagiario_form.html'
    success_url = reverse_lazy('estagiarios')

    def form_valid(self, form):
        for field_name, field_value in form.cleaned_data.items():
            item = form.cleaned_data[field_name]
            if field_name not in ['outrasinformacoes', 'biografia']:
                if not item:
                    messages.error(self.request, "O Campo'" + field_name + "'é obrigatorio")
                    return self.render_to_response(self.get_context_data(form=form))

        nome = form.cleaned_data['first_name']
        sobrenome = form.cleaned_data['last_name']
        username = f"{nome.replace(' ', '-')}-{sobrenome.replace(' ', '-')}"

        user = User.objects.filter(username=username)
        if user:
            messages.error(self.request, "Usuário já existe.")
            return self.render_to_response(self.get_context_data(form=form))



        response = super().form_valid(form)
        email = self.object.email
        senha = secrets.token_urlsafe(6)
        self.object.password = make_password(senha)
        self.object.save()
        messages.info(self.request, f"Estagiario criado com sucesso. <br> Email do usuário: {email} <br> Senha do usuário: { senha }", )
        return response


    def form_invalid(self, form):
        errors = form.errors.as_text()
        messages.error(self.request, "Erro ao criar estagiário. Por favor, corrija os erros no formulário")
        return render(self.request, self.template_name, {'form': form})


@method_decorator(user_passes_test(is_supervisor_orientador, login_url='/ERRO'), name='dispatch')
class EstagiarioList(ListView):
    model = Estagiario
    template_name = 'estagiarioTemplate/estagiario_list.html'
    context_object_name = 'estagiarios'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        role_do_usuario = self.request.user.role

        estagiarios_ativos = Estagiario.objects.filter(is_active=True)
        estagiarios_desativados = Estagiario.objects.filter(is_active=False)

        if query:
            estagiarios_ativos = estagiarios_ativos.filter(username__icontains=query.replace(' ', '-'))
            estagiarios_desativados = estagiarios_desativados.filter(username__icontains=query.replace(' ', '-'))

        if role_do_usuario == 'SUPERVISOR':
            estagiarios = estagiarios_ativos.union(estagiarios_desativados)
        else:
            estagiarios = estagiarios_ativos

        estagiarios = estagiarios.order_by('-is_active')

        return estagiarios

@method_decorator(user_passes_test(is_supervisor_orientador, login_url='/ERRO'), name='dispatch')
class EstagiarioEdit(UpdateView):
    model = Estagiario
    template_name = 'estagiarioTemplate/estagiario_form.html'
    form_class = EstagiarioFormEdit

    def form_valid(self, form):
        for field_name, field_value in form.cleaned_data.items():
            item = form.cleaned_data[field_name]
            if field_name not in ['outrasinformacoes', 'biografia']:
                if not item:
                    messages.error(self.request, "O Campo'" + field_name + "'é obrigatorio")
                    return self.render_to_response(self.get_context_data(form=form))

        messages.success(self.request, "Estagiario atualizado com sucesso.")
        return super().form_valid(form)

@method_decorator(user_passes_test(is_supervisor_orientador, login_url='/ERRO'), name='dispatch')
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


@method_decorator(user_passes_test(is_estagiario, login_url='/ERRO'), name='dispatch')
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

