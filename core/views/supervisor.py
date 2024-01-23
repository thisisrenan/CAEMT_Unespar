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

class SupervisorEditProfile(UpdateView):
    model = User
    context_object_name = 'userProfile'
    fields = ['first_name', 'last_name', 'biografia', 'outrasinformacoes']
    template_name = 'perfiledit/perfilEdit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('edit_profile')


