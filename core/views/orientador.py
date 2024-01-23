

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
from core.models.users import Orientador

from .core import is_supervisor

class OrientadorCreate(CreateView):
    model = Orientador
    form_class = OrientadorForm
    template_name = 'orientadoreTemplate/orientador_form.html'
    success_url = reverse_lazy('orientadores')

    def form_valid(self, form):
        messages.success(self.request, "Orientador criado com sucesso.")
        return super().form_valid(form)


class OrientadorList(ListView):
    model = Orientador
    template_name = 'orientadoreTemplate/orientador_list.html'
    context_object_name = 'orientadores'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            orinetador = Orientador.objects.filter(username__icontains=query)
        else:
            orientador = Orientador.objects.all()

        return orientador.order_by('-is_active')

class OrientadorEdit(UpdateView):
    model = Orientador
    template_name = 'orientadoreTemplate/orientador_form.html'
    form_class = OrientadorFormEdit
    success_url = reverse_lazy('orientadores')

    def form_valid(self, form):
        messages.success(self.request, "Orientador atualizado com sucesso.")
        return super().form_valid(form)



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

