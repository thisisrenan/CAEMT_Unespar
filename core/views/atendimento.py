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
from datetime import datetime

from django.contrib.auth.views import PasswordChangeView

from core.models import User
from core.models.users import UserActivity, Atendimentos, agenda, Participante


def presencaFalta(request):
    if request.method == 'POST':
        participante = request.POST.get("participante")

        data = request.POST.get("data")
        motivo = request.POST.get("motivo")

        atendimento = Atendimentos.objects.get(participante=participante, data_atendimento=data)
        atendimento.motivoFalta = motivo
        atendimento.ocorreu = True
        atendimento.save()

        participanteObj = Participante.objects.get(pk=participante)
        participanteObj.qtd_atendimentos += 1
        participanteObj.save()
        messages.success(request, "presença feita com sucesso")

    return redirect("home")