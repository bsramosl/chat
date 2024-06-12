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
                form = UnidadEducativaForm(request.POST)
                if form.is_valid():
                    item = UnidadEducativa(nombre = form.cleaned_data['nombre'],
                                direccion = form.cleaned_data['direccion'],
                                telefono = form.cleaned_data['telefono'],                                )

                    item.save()
                    messages.success(request, 'Registro guardado con éxito.')
                    res_json = {"result": False}
                    return redirect(request.META.get('HTTP_REFERER', ''))
                else:
                    res_json = {'result': True, "mensaje": "Error en el formulario: {}".format([{k: v[0]} for k, v in form.errors.items()])}
            except Exception as ex:
                transaction.set_rollback(True)
                res_json = {'result': True, "mensaje": "Error: {}".format(ex)}
            return JsonResponse(res_json, safe=False)


        elif action == 'editar':

            try:

                with transaction.atomic():
                    vendedor = UnidadEducativa.objects.get(pk=request.POST['id'])
                    form = UnidadEducativaForm(request.POST)
                    if form.is_valid():
                        vendedor.nombre = form.cleaned_data['nombre']
                        vendedor.direccion = form.cleaned_data['direccion']
                        vendedor.telefono = form.cleaned_data['telefono']
                        vendedor.save()
                        messages.success(request, 'Registro guardado con éxito.')
                        res_json = {"result": False}
                        return redirect(request.META.get('HTTP_REFERER', ''))
                    else:
                        res_json = {'result': True, "mensaje": "Error en el formulario: {}".format(
                            [{k: v[0]} for k, v in form.errors.items()])}
            except Exception as ex:
                transaction.set_rollback(True)
                res_json = {'result': True, "mensaje": "Error: {}".format(ex)}
            return JsonResponse(res_json, safe=False)

        elif action == 'eliminar':
            try:
                item = UnidadEducativa.objects.get(pk=request.POST['id'])
                item.delete()
                messages.success(request, 'Registro eliminado con éxito.')
                return redirect(request.META.get('HTTP_REFERER', ''))
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
                    form = UnidadEducativaForm()
                    data['form'] = form
                    template = get_template("unidadeducativa/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            elif action == 'editar':
                try:
                    data['id'] = request.GET['id']
                    data['action'] = 'editar'
                    data['item'] = item = UnidadEducativa.objects.get(pk=request.GET['id'])
                    initial = model_to_dict(item)
                    form = UnidadEducativaForm(initial=initial)
                    data['form'] = form
                    template = get_template("unidadeducativa/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    pass
            return HttpResponseRedirect(request.path)

        else:
            try:
                data['title'] = 'Administración Unidad Educativa'
                data['title1'] = 'Unidad Educativa'
                filtros,s, url_vars, id = Q(), request.GET.get('s', ''),'', request.GET.get('id', '0')
                eItems = UnidadEducativa.objects.all()
                data['items'] = eItems
                data['url_vars'] = url_vars
                return render(request, "unidadeducativa/view.html", data)
            except Exception as ex:
                pass