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

        if action == 'agregar':
            try:
                form = CursoForm(request.POST)
                if form.is_valid():
                    item = Curso(nombre = form.cleaned_data['nombre'],
                                unidad_educativa = form.cleaned_data['unidad_educativa'],
                                profesor = form.cleaned_data['profesor']
                                )

                    item.save()
                    res_json = {'result': False, "mensaje": "Registro guardado con éxito."}
                else:
                    res_json = {'result': True, "mensaje": "Error en el formulario: {}".format([{k: v[0]} for k, v in form.errors.items()])}
            except Exception as ex:
                transaction.set_rollback(True)
                res_json = {'result': True, "mensaje": "Error: {}".format(ex)}
            return JsonResponse(res_json, safe=False)


        elif action == 'editar':

            try:

                with transaction.atomic():
                    vendedor = Curso.objects.get(pk=request.POST['id'])
                    form = CursoForm(request.POST)
                    if form.is_valid():
                        actualizar_instancia_con_form(vendedor,form)
                        res_json = {'result': False, "mensaje": "Registro guardado con éxito."}
                    else:
                        res_json = {'result': True, "mensaje": "Error en el formulario: {}".format(
                            [{k: v[0]} for k, v in form.errors.items()])}
            except Exception as ex:
                transaction.set_rollback(True)
                res_json = {'result': True, "mensaje": "Error: {}".format(ex)}
            return JsonResponse(res_json, safe=False)

        elif action == 'eliminar':
            try:
                item = Curso.objects.get(pk=request.POST['id'])
                item.delete()
                res_json = {"result": False, 'message': 'Registro eliminado con éxito.'}
                return JsonResponse(res_json, safe=False)
            except Exception as ex:
                transaction.set_rollback(True)
                res_json = {'result': True, "mensaje": "Error: {}".format(ex)}
            return JsonResponse(res_json, safe=False)

        return JsonResponse({"result": "bad", "mensaje": u"Solicitud Incorrecta."})
    else:
        if 'action' in request.GET:
            action = request.GET['action']

            if action == 'agregar':
                try:
                    data['action'] = 'agregar'
                    form = CursoForm()
                    data['form'] = form
                    template = get_template("curso/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            elif action == 'editar':
                try:
                    data['id'] = request.GET['id']
                    data['action'] = 'editar'
                    data['item'] = item = Curso.objects.get(pk=request.GET['id'])
                    initial = model_to_dict(item)
                    form = CursoForm(initial=initial)
                    data['form'] = form
                    template = get_template("curso/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            return HttpResponseRedirect(request.path)

        else:
            try:
                data['title'] = 'Administración de Cursos'
                data['title1'] = 'Curso'
                eItems = Curso.objects.all()
                data['items'] = eItems
                return render(request, "curso/view.html", data)
            except Exception as ex:
                pass