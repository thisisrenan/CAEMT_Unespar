

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.contrib.auth.views import PasswordChangeView

from core.models import User


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

#edit perfil
class SupervisorEditImage(UpdateView):
    model = User
    context_object_name = 'userProfile'
    fields = ['image']
    template_name = 'perfiledit/perfilEdit.html'
    def get_object(self, queryset=None):
            return self.request.user

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
