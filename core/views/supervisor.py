import secrets

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.views import View

from core.forms import SupervisorForm, SupervisorFormEdit
from core.models import User

from .core import *

@method_decorator(user_passes_test(is_supervisor, login_url='/ERRO'), name='dispatch')
class SupervisorCreate(CreateView):
    model = User
    form_class = SupervisorForm
    context_object_name = 'supervisores'
    template_name = 'supervisorTemplate/supervisor_form.html'
    success_url = reverse_lazy('supervisores')

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
        print(senha)
        self.object.password = make_password(senha)
        self.object.save()
        messages.info(self.request, f"Supervisor criado com sucesso. <br> Email do usuário: {email} <br> Senha do usuário: { senha }", )
        return response


@method_decorator(user_passes_test(is_supervisor, login_url='/ERRO'), name='dispatch')
class SupervisorList(ListView):
    model = User
    template_name = 'supervisorTemplate/supervisor_list.html'
    context_object_name = 'supervisores'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return User.objects.filter(username__icontains=query, role='SUPERVISOR')
        return User.objects.filter(role='SUPERVISOR')

@method_decorator(user_passes_test(is_supervisor, login_url='/ERRO'), name='dispatch')
class SupervisorEdit(UpdateView):
    model = User
    context_object_name = 'supervisores'
    template_name = 'supervisorTemplate/supervisor_form.html'
    form_class = SupervisorFormEdit

    def form_valid(self, form):
        for field_name, field_value in form.cleaned_data.items():
            item = form.cleaned_data[field_name]
            if field_name not in ['outrasinformacoes', 'biografia']:
                if not item:
                    messages.error(self.request, "O Campo'" + field_name + "'é obrigatorio")
                    return self.render_to_response(self.get_context_data(form=form))

        messages.success(self.request, "Supervisor atualizado com sucesso.")
        return super().form_valid(form)

@method_decorator(user_passes_test(is_supervisor, login_url='/ERRO'), name='dispatch')
class SupervisorDelete(View):
    success_url = reverse_lazy('supervisores')

    def get(self, request, pk):
        supervisor = get_object_or_404(User, pk=pk)
        return render(request, self.template_name, {'supervisor': supervisor})

    def post(self, request, pk):
        supervisor = get_object_or_404(User, pk=pk)
        supervisor.is_active = False
        supervisor.save()

        messages.success(request, "Supervisor excluído com sucesso.")
        return redirect(self.success_url)


#edit Perfil
@method_decorator(user_passes_test(is_supervisor, login_url='/ERRO'), name='dispatch')
class SupervisorEditProfile(UpdateView):
    model = User
    context_object_name = 'userProfile'
    fields = ['first_name', 'last_name', 'biografia', 'outrasinformacoes']
    template_name = 'perfiledit/perfilEdit.html'

    def get_object(self, queryset=None):
        return self.request.user
    def form_valid(self, form):

        messages.success(self.request, "Perfil atualizado com sucesso.")
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('edit_profile')


