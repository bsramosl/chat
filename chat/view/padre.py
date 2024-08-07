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
                form = PadreForm(request.POST)
                if form.is_valid():
                    user = User.objects.create_user((form.cleaned_data['nombre'].split()[0] + form.cleaned_data['apellidos'].split()[0]),
                                                    form.cleaned_data['email'],
                                                    form.cleaned_data['cedula'],
                                                    first_name=form.cleaned_data['nombre'],
                                                    last_name=form.cleaned_data['apellidos'])
                    user.save()
                    item = Persona(nombre = form.cleaned_data['nombre'],
                                apellidos = form.cleaned_data['apellidos'],
                                cedula = form.cleaned_data['cedula'],
                                nacimiento = form.cleaned_data['nacimiento'],
                                sexo = form.cleaned_data['sexo'],
                                telefono = form.cleaned_data['telefono'],
                                email = form.cleaned_data['email'],
                                usuario = user,
                                unidad_educativa = form.cleaned_data['unidad_educativa'],
                                tipo = 'Padre')

                    item.save()
                    res_json = {'result': False, "mensaje": "Registro guardado con éxito."}
                else:
                    res_json = {'result': True, "mensaje": "Error en el formulario: {}".format([{k: v[0]} for k, v in form.errors.items()])}
            except Exception as ex:
                transaction.set_rollback(True)
                res_json = {'result': True, "mensaje": "Error: {}".format(ex)}
            return JsonResponse(res_json, safe=False)

        if action == 'hijo':
            try:
                form = ParentescoForm(request.POST)
                if form.is_valid():
                    item = Parentesco(padre_id=int(request.POST['id']),
                                   hijo=form.cleaned_data['alumno']
                                      )
                    item.save()
                    res_json = {'result': False, "mensaje": "Registro guardado con éxito."}
                else:
                    res_json = {'result': True, "mensaje": "Error en el formulario: {}".format(
                        [{k: v[0]} for k, v in form.errors.items()])}
            except Exception as ex:
                transaction.set_rollback(True)
                res_json = {'result': True, "mensaje": "Error: {}".format(ex)}
            return JsonResponse(res_json, safe=False)


        elif action == 'editar':

            try:
                with transaction.atomic():
                    vendedor = Persona.objects.get(pk=request.POST['id'])
                    form = PadreForm(request.POST)
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
                item = Persona.objects.get(pk=request.POST['id'])
                user = User.objects.get(id=item.usuario_id)
                item.delete()
                user.delete()
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
                    form = PadreForm()
                    form.quitar()
                    data['form'] = form
                    template = get_template("padre/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if action == 'hijo':
                try:
                    data['action'] = 'hijo'
                    data['id'] = request.GET['id']
                    form = ParentescoForm()
                    data['form'] = form
                    template = get_template("padre/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            elif action == 'editar':
                try:
                    data['id'] = request.GET['id']
                    data['action'] = 'editar'
                    data['item'] = item = Persona.objects.get(pk=request.GET['id'])
                    initial = model_to_dict(item)
                    initial.update(model_to_dict(item.usuario))
                    form = PadreForm(initial=initial)
                    form.quitar()
                    data['form'] = form
                    template = get_template("padre/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            elif action == 'editar':
                try:
                    data['id'] = request.GET['id']
                    data['action'] = 'editar'
                    data['item'] = item = Persona.objects.get(pk=request.GET['id'])
                    initial = model_to_dict(item)
                    initial.update(model_to_dict(item.usuario))
                    form = PadreForm(initial=initial)
                    form.quitar()
                    data['form'] = form
                    template = get_template("padre/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            return HttpResponseRedirect(request.path)

        else:
            try:
                data['title'] = 'Administración de Padres'
                data['title1'] = 'Padres'
                eItems = Persona.objects.filter(tipo='Padre')
                data['items'] = eItems
                return render(request, "padre/view.html", data)
            except Exception as ex:
                pass