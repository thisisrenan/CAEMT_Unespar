from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
# Create your views here.
def index(request):
    return render(request, 'registration/login.html', {})

@login_required
def home(request):
    return render(request, "index.html", {})