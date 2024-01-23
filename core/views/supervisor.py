from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from core.forms import SupervisorForm, SupervisorFormEdit
from core.models import User

from .core import is_supervisor

class SupervisorCreate(CreateView):
    model = User
    form_class = SupervisorForm
    context_object_name = 'supervisores'
    template_name = 'supervisorTemplate/supervisor_form.html'
    success_url = reverse_lazy('supervisores')


@method_decorator(user_passes_test(is_supervisor, login_url='home'), name='dispatch')
class SupervisorList(ListView):
    model = User
    template_name = 'supervisorTemplate/supervisor_list.html'
    context_object_name = 'supervisores'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return User.objects.filter(username__icontains=query, role='SUPERVISOR')
        return User.objects.filter(role='SUPERVISOR')

class SupervisorEdit(UpdateView):
    model = User
    context_object_name = 'supervisores'
    template_name = 'supervisorTemplate/supervisor_form.html'
    form_class = SupervisorFormEdit

class SupervisorDelete(DeleteView):
    model = User
    context_object_name = 'supervisores'
    template_name = 'supervisorTemplate/supervisor_confirm_delete.html'
    success_url = reverse_lazy('supervisores')


#edit Perfil

class SupervisorEditProfile(UpdateView):
    model = User
    context_object_name = 'userProfile'
    fields = ['first_name', 'last_name', 'biografia', 'outrasinformacoes']
    template_name = 'perfiledit/perfilEdit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('edit_profile')
