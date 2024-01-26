

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.contrib.auth.views import PasswordChangeView

from core.models import User
from core.models.users import UserActivity


def is_supervisor(user):
    return user.is_authenticated and user.role == 'SUPERVISOR'

def is_orientador(user):
    return user.is_authenticated and user.role == 'ORIENTADOR'

def is_estagiario(user):
    return user.is_authenticated and user.role == 'ESTAGIARIO'


def get_logged_in_users():
    users_activity = UserActivity.objects.all().order_by('-last_activity')

    return users_activity

def index(request):

    return render(request, 'registration/login.html', {})

@login_required
def home(request):
    users = get_logged_in_users()
    print(users)
    return render(request, "index.html", {"users":users})

@login_required
def PerfilProfile(request, username):
    user = get_object_or_404(User,username=username)
    context = {
        "userProfile": user
    }
    return render(request, 'perfil/perfil.html', context)

#edit perfil
def reativarUsuario(request, pk):
    user = get_object_or_404(User, id=pk)
    user.is_active = True
    user.save()
    messages.success(request, f"{user.role.capitalize()} ativado com sucesso.")


    referer = request.META.get('HTTP_REFERER')

    if referer:
        return HttpResponseRedirect(referer)
    else:
        return HttpResponseRedirect(reverse('home'))




class SupervisorEditImage(UpdateView):
    model = User
    context_object_name = 'userProfile'
    fields = ['image']
    template_name = 'perfiledit/perfilEdit.html'
    def get_object(self, queryset=None):
            return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Imagem atualizada com sucesso.")
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('edit_photo')


class SupervisorChangePasswordView(PasswordChangeView):
    template_name = 'perfiledit/changePassword.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('edit_profile')




