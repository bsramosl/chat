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
                    item = Padre(nombre = form.cleaned_data['nombre'],
                                apellidos = form.cleaned_data['apellidos'],
                                cedula = form.cleaned_data['cedula'],
                                nacimiento = form.cleaned_data['nacimiento'],
                                sexo = form.cleaned_data['sexo'],
                                telefono = form.cleaned_data['telefono'],
                                email = form.cleaned_data['email'],
                                usuario = user,
                                unidad_educativa = form.cleaned_data['unidad_educativa'],
                                alumno = form.cleaned_data['alumno'])

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
                    vendedor = Padre.objects.get(pk=request.POST['id'])
                    form = PadreForm(request.POST,instance=vendedor)
                    if form.is_valid():
                        form.save()
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
                item = Padre.objects.get(pk=request.POST['id'])
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
                    form = PadreForm()
                    data['form'] = form
                    template = get_template("padre/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            elif action == 'editar':
                try:
                    data['id'] = request.GET['id']
                    data['action'] = 'editar'
                    data['item'] = item = Padre.objects.get(pk=request.GET['id'])
                    initial = model_to_dict(item)
                    initial.update(model_to_dict(item.usuario))
                    form = PadreForm(initial=initial)
                    data['form'] = form
                    template = get_template("padre/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            return HttpResponseRedirect(request.path)

        else:
            try:
                request.session
                data['title'] = 'Ajustes'
                data['title1'] = 'Perfil'
                filtros,s, url_vars, id = Q(), request.GET.get('s', ''),'', request.GET.get('id', '0')
                eItems = User.objects.filter()
                data['paging'] = paging
                data['page'] = page
                data['rangospaging'] = paging.rangos_paginado(p)
                data['items'] = page.object_list
                data['url_vars'] = url_vars
                return render(request, "ajustes/view.html", data)
            except Exception as ex:
                pass