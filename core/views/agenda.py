from datetime import datetime, timedelta
from django.shortcuts import render, redirect,HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Q
from core.models.users import agenda, Participante, Estagiario
from .core import is_supervisor, is_supervisor_orientador


@user_passes_test(is_supervisor_orientador, login_url='/ERRO')
def horario_reservado(self, horario, reserva):
    return self.horario == horario

@user_passes_test(is_supervisor_orientador, login_url='/ERRO')
def rediAgenda(request):
    dias_semana = {
        0: 'SEGUNDA-FEIRA',
        1: 'TERÇA-FEIRA',
        2: 'QUARTA-FEIRA',
        3: 'QUINTA-FEIRA',
        4: 'SEXTA-FEIRA',
        5: 'SÁBADO',
        6: 'DOMINGO',
    }

    hoje = datetime.now().date()
    dia_da_semana_atual = hoje.weekday()
    dia = dias_semana[dia_da_semana_atual]

    return redirect('agenda/' + dia)

@user_passes_test(is_supervisor_orientador, login_url='/ERRO')
def agendaHome(request, semana):
    dia_da_semana_valor = [x[0] for x in agenda.SEMANA_CHOICES if x[1].upper() == semana.upper()]

    if dia_da_semana_valor:
        horarios_reservados = agenda.objects.filter(dia_da_semana=dia_da_semana_valor[0]).order_by('horario')

        dias_semana = {
            0: 'SEGUNDA-FEIRA',
            1: 'TERÇA-FEIRA',
            2: 'QUARTA-FEIRA',
            3: 'QUINTA-FEIRA',
            4: 'SEXTA-FEIRA',
            5: 'SÁBADO',
            6: 'DOMINGO',
        }
        horarios = agenda.HORARIO_CHOICES
        horarios_formatados = [horario[0].strftime('%H:%M:%S') for horario in horarios]

        hoje = datetime.now().date()
        dia_da_semana_atual = hoje.weekday()
        datas_semana = {
            dias_semana[(i) % 7]: {
                'dia': (hoje + timedelta(days=i)).day,
                'data_completa': hoje + timedelta(days=i),
            }
            for i in range(7)
        }
        dia = dias_semana[dia_da_semana_valor[0]]



        j = 0
        horariosAux = []

        for i in range(len(horarios_formatados)):
            if j < len(horarios_reservados) and str(horarios_reservados[j].horario) == str(horarios_formatados[i]):
                horario_sem_segundos = horarios_formatados[i].split(":")[:-1]
                horariosAux.append({"reserva": True, "info": horarios_reservados[j],"hora": ":".join(horario_sem_segundos)})
                j += 1
            else:
                horario_sem_segundos = horarios_formatados[i].split(":")[:-1]
                horariosAux.append({"reserva": False, "hora": ":".join(horario_sem_segundos)})

        participantes_sem_agenda = Participante.objects.annotate(num_agendas=Count('agendas_participante')).filter(num_agendas=0)
        estagiarios_sem_agenda = Estagiario.objects.annotate(num_agendas=Count('agendas_estagiario')).filter(
            Q(num_agendas=0)  & Q(is_active=1) | (Q(num_agendas=1) & Q(ano_letivo__gt=3) & Q(is_active=1))
        )


        context = {
            "horarios_reservados": horariosAux,
            "estagiarios_sem_agenda": estagiarios_sem_agenda,
            "participantes_sem_agenda": participantes_sem_agenda,
            "dia": dia,
            "datas_semana": datas_semana,
        }
        return render(request, "agenda/index.html", context)
    else:
        return HttpResponse("Dia da semana inválido. Página de erro aqui.")

@user_passes_test(is_supervisor_orientador, login_url='/ERRO')
def criar_agenda(request):
    if request.method == 'POST':
        semana = request.POST.get("semana")
        dia_da_semana= 0
        horario = request.POST.get("horario")
        estagiario = Estagiario.objects.get(id=request.POST.get("estagiario"))
        participante = Participante.objects.get(id=request.POST.get("participante"))

        agenda_existente = agenda.objects.filter(participante=participante).first()

        if agenda_existente:
            agenda_existente.delete()

        for numero, nome in agenda.SEMANA_CHOICES:
            if nome.lower() == semana.lower():
                dia_da_semana = numero

        nova_agenda = agenda.objects.create(
            dia_da_semana=dia_da_semana,
            horario=horario,
            participante=participante,
            reservadoPor = request.user
        )
        nova_agenda.estagiario.add(estagiario)

        nova_agenda.save()
        messages.success(request, "Agendado com sucesso.")
        if request.POST.get('edit') == 'True':
            return redirect(reverse('Participante_perfil', args=[participante.username]))
        else:
            return redirect(reverse('agenda', args=[semana]))

@user_passes_test(is_supervisor_orientador, login_url='/ERRO')
def deletar_agenda(request,pk):
    semana = request.POST.get("semana")
    agendamento = agenda.objects.get(id=pk)
    agendamento.delete()
    messages.success(request, "Agendamento deletado com sucesso.")
    return redirect(reverse('agenda', args=[semana]))


@user_passes_test(is_supervisor_orientador, login_url='/ERRO')
def agendaEdit(request, semana, username):
    dia_da_semana_valor = [x[0] for x in agenda.SEMANA_CHOICES if x[1].upper() == semana.upper()]
    try:
        participante = Participante.objects.get(username=username)
    except Participante.DoesNotExist:
        participante = False
    if dia_da_semana_valor and participante:
        horarios_reservados = agenda.objects.filter(dia_da_semana=dia_da_semana_valor[0]).order_by('horario')

        dias_semana = {
            0: 'SEGUNDA-FEIRA',
            1: 'TERÇA-FEIRA',
            2: 'QUARTA-FEIRA',
            3: 'QUINTA-FEIRA',
            4: 'SEXTA-FEIRA',
            5: 'SÁBADO',
            6: 'DOMINGO',
        }
        horarios = agenda.HORARIO_CHOICES
        horarios_formatados = [horario[0].strftime('%H:%M:%S') for horario in horarios]

        hoje = datetime.now().date()
        dia_da_semana_atual = hoje.weekday()
        datas_semana = {
            dias_semana[(i) % 7]: {
                'dia': (hoje + timedelta(days=i)).day,
                'data_completa': hoje + timedelta(days=i),
            }
            for i in range(7)
        }
        dia = dias_semana[dia_da_semana_valor[0]]



        j = 0
        horariosAux = []

        for i in range(len(horarios_formatados)):
            if j < len(horarios_reservados) and str(horarios_reservados[j].horario) == str(horarios_formatados[i]):
                horario_sem_segundos = horarios_formatados[i].split(":")[:-1]
                horariosAux.append({"reserva": True, "info": horarios_reservados[j],"hora": ":".join(horario_sem_segundos)})
                j += 1
            else:
                horario_sem_segundos = horarios_formatados[i].split(":")[:-1]
                horariosAux.append({"reserva": False, "hora": ":".join(horario_sem_segundos)})


        agenda_do_participante = agenda.objects.filter(participante=participante)



        estagiarios_sem_agenda = Estagiario.objects.annotate(num_agendas=Count('agendas_estagiario')).filter(
            Q(num_agendas=0)  & Q(is_active=1) | (Q(num_agendas=1) & Q(ano_letivo__gt=3) & Q(is_active=1))
        )
        agenda_participante = agenda_do_participante.first()
        if agenda_participante:
            estagiario_da_agenda = agenda_do_participante.first().estagiario.all()
            estagiarios_sem_agenda = list(estagiario_da_agenda) + list(estagiarios_sem_agenda)

        context = {
            "horarios_reservados": horariosAux,
            "estagiarios_sem_agenda": estagiarios_sem_agenda,
            "participantes_sem_agenda": [participante],
            "dia": dia,
            "datas_semana": datas_semana,
            "users": participante.username,
        }
        return render(request, "agenda/index.html", context)

    else:
        return HttpResponse("Dia da semana inválido. Página de erro aqui.")
