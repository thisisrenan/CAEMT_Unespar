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


from core.forms import OrientadorForm, OrientadorFormEdit
from core.models.users import Orientador, User

from .core import *
@method_decorator(user_passes_test(is_supervisor, login_url='/ERRO'), name='dispatch')
class OrientadorCreate(CreateView):
    model = Orientador
    form_class = OrientadorForm
    template_name = 'orientadoreTemplate/orientador_form.html'
    success_url = reverse_lazy('orientadores')

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
        messages.info(self.request, f"Orientador criado com sucesso. <br> Email do usuário: {email} <br> Senha do usuário: { senha }", )
        return response

@method_decorator(user_passes_test(is_supervisor, login_url='/ERRO'), name='dispatch')
class OrientadorList(ListView):
    model = Orientador
    template_name = 'orientadoreTemplate/orientador_list.html'
    context_object_name = 'orientadores'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            orientador = Orientador.objects.filter(username__icontains=query.replace(' ', '-'))
        else:
            orientador = Orientador.objects.all()

        return orientador.order_by('-is_active')


@method_decorator(user_passes_test(is_supervisor, login_url='/ERRO'), name='dispatch')
class OrientadorEdit(UpdateView):
    model = Orientador
    template_name = 'orientadoreTemplate/orientador_form.html'
    form_class = OrientadorFormEdit
    success_url = reverse_lazy('orientadores')

    def form_valid(self, form):
        for field_name, field_value in form.cleaned_data.items():
            item = form.cleaned_data[field_name]
            if field_name not in ['outrasinformacoes', 'biografia']:
                if not item:
                    messages.error(self.request, "O Campo'" + field_name + "'é obrigatorio")
                    return self.render_to_response(self.get_context_data(form=form))

        messages.success(self.request, "Orientador atualizado com sucesso.")
        return super().form_valid(form)


@method_decorator(user_passes_test(is_supervisor, login_url='/ERRO'), name='dispatch')
class OrientadorDelete(View):
    success_url = reverse_lazy('orientadores')

    def get(self, request, pk):
        orientador = get_object_or_404(Orientador, pk=pk)
        return render(request, self.template_name, {'orientador': orientador})

    def post(self, request, pk):
        estagiario = get_object_or_404(Orientador, pk=pk)
        estagiario.is_active = False
        estagiario.save()

        messages.success(request, "Orientador excluído com sucesso.")
        return redirect(self.success_url)

#edit Perfil
@method_decorator(user_passes_test(is_orientador, login_url='/ERRO'), name='dispatch')
class OrientadorEditProfile(UpdateView):
    model = Orientador
    context_object_name = 'userProfile'
    fields =['first_name', 'last_name','telefone','biografia', 'outrasinformacoes','data_de_nascimento']
    template_name = 'perfiledit/perfilEdit.html'

    def get_object(self, queryset=None):
        return self.request.user.orientador

    def get_success_url(self):
        return reverse_lazy('edit_profile')

    def form_valid(self, form):
        messages.success(self.request, "Perfil Editado com sucesso.")
        return super().form_valid(form)

