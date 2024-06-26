# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from chat.forms import *
from chat.funciones import *
from chat.models import *
from datetime import datetime
from django.db.models import Max
from django.template.loader import get_template
from django.db.models import Q
from django.contrib import messages


@login_required(redirect_field_name='ret', login_url='/login')
# @secure_module
# @last_access
@transaction.atomic()
def view(request):
    data = {}
    data['usuario'] = usuario = request.session['usuario']
   #cargar_plantilla_base_simple(request, data)
    hoy = datetime.now().date()
    if request.method == 'POST':
        action = request.POST['action']

        return JsonResponse({"result": "bad", "mensaje": u"Solicitud Incorrecta."})
    else:
        if 'action' in request.GET:
            action = request.GET['action']


            return HttpResponseRedirect(request.path)

        else:
            try:
                data['title'] = 'Perfil'
                data['persona'] = persona = Persona.objects.get(pk=usuario['id_per'])
                hijos = Parentesco.objects.filter(padre=persona)
                data['hijosc'] = hijos.count()
                if hijos.count():
                    data['hijos'] = Persona.objects.filter(pk__in=hijos.values_list('hijo', flat=True))
                if usuario['tipo'] == 'Alumno':
                    data['cursos'] = Matricula.objects.filter(alumno=persona)
                elif usuario['tipo'] == 'Profesor' :
                    data['cursos'] = Curso.objects.filter(profesor=persona)
                elif usuario['tipo'] == 'Administrador':
                    data['tipos'] = Persona.objects.values('tipo').annotate(total=Count('tipo'))

                return render(request, "perfil/view.html", data)
            except Exception as ex:
                pass