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

            if action == 'materia':
                try:
                    data['materias'] = obtener_materias_y_notas_por_curso(request.GET['id'])
                    return render(request, "curso/materias.html", data)
                except Exception as ex:
                    pass


            return HttpResponseRedirect(request.path)

        else:
            try:
                data['title'] = 'Perfil'
                usuario = request.session['usuario']
                filtros,s, url_vars, id = Q(), request.GET.get('s', ''),'', request.GET.get('id', '0')
                user = Persona.objects.get(pk=usuario['id'])
                data['cursos'] = Curso.objects.filter(profesor=user)

                return render(request, "curso/cursos.html", data)
            except Exception as ex:
                pass