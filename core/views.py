from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse, reverse_lazy

from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .forms import OrientadorForm, OrientadorFormEdit, EstagiarioForm, EstagiarioFormEdit, SupervisorForm, SupervisorFormEdit

from core.models.users import *
from django.views import generic


def is_supervisor(user):
    return user.is_authenticated and user.role == 'SUPERVISOR'

def index(request):
    return render(request, 'registration/login.html', {})

@login_required
def home(request):
    return render(request, "index.html", {})

@login_required
def PerfilProfile(request, username):
    user = get_object_or_404(User,username=username)
    context = {
        "userProfile": user
    }
    return render(request, 'perfil/perfil.html', context)

class OrientadorCreate(CreateView):
    model = Orientador
    form_class = OrientadorForm
    template_name = 'orientadoreTemplate/orientador_form.html'
    success_url = reverse_lazy('orientadores')


@method_decorator(user_passes_test(is_supervisor, login_url='home'), name='dispatch')
class OrientadorList(ListView):
    model = Orientador
    template_name = 'orientadoreTemplate/orientador_list.html'
    context_object_name = 'orientadores'


    def get_queryset(self):
        return Orientador.objects.all()

class OrientadorEdit(UpdateView):
    model = Orientador
    template_name = 'orientadoreTemplate/orientador_form.html'
    form_class = OrientadorFormEdit

class OrientadorDelete(DeleteView):
    model = Orientador
    context_object_name = 'orientadores'
    template_name = 'orientadoreTemplate/orientador_confirm_delete.html'
    success_url = reverse_lazy('orientadores')



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

class SupervisorCreate(CreateView):
    model = User
    form_class = SupervisorForm
    template_name = 'supervisorTemplate/supervisor_form.html'
    success_url = reverse_lazy('supervisores')


@method_decorator(user_passes_test(is_supervisor, login_url='home'), name='dispatch')
class SupervisorList(ListView):
    model = User
    template_name = 'supervisorTemplate/supervisor_list.html'
    context_object_name = 'supervisores'


    def get_queryset(self):
        return User.objects.all()

class SupervisorEdit(UpdateView):
    model = User
    template_name = 'supervisorTemplate/supervisor_form.html'
    form_class = SupervisorFormEdit

class SupervisorDelete(DeleteView):
    model = User
    context_object_name = 'supervisores'
    template_name = 'supervisorTemplate/supervisor_confirm_delete.html'
    success_url = reverse_lazy('supervisores')