from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .forms import OrientadorForm

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
    template_name = 'core/orientador_form.html'
    success_url = 'home'

@method_decorator(user_passes_test(is_supervisor, login_url='home'), name='dispatch')
class OrientadorList(ListView):
    model = Orientador
    template_name = 'core/orientador_list.html'
    context_object_name = 'orientadores'


    def get_queryset(self):
        return Orientador.objects.all()
