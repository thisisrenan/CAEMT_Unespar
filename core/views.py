from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.models.users import *
from django.views import generic

# Create your views here.
# Create your views here.
def index(request):
    return render(request, 'registration/login.html', {})

@login_required
def home(request):
    return render(request, "index.html", {})

def PerfilProfile(request, username):
    user = get_object_or_404(User,username=username)
    context = {
        "user": user
    }
    return render(request, 'perfil/perfil.html', context)