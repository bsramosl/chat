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

        if action == 'editardatos':
            try:
                with transaction.atomic():
                    vendedor = Persona.objects.get(usuario_id=usuario['id'])
                    form = PersonaForm(request.POST)
                    if form.is_valid():
                        actualizar_instancia_con_form(vendedor,form)
                        messages.success(request, 'Registro guardado con éxito.')
                        res_json = {"result": True,"mensaje": "Datos Actualizados"}
                        return JsonResponse(res_json, safe=False)
                    else:
                        res_json = {'result': False, "mensaje": "Error en el formulario: {}".format(
                            [{k: v[0]} for k, v in form.errors.items()])}
                        return JsonResponse(res_json, safe=False)
            except Exception as ex:
                transaction.set_rollback(True)
                res_json = {'result': True, "mensaje": "Error: {}".format(ex)}
            return JsonResponse(res_json, safe=False)

        if action == 'editarcontraseña':

            try:
                user = User.objects.get(pk=usuario['id'])
                password_form = CustomPasswordChangeForm(user=user, data=request.POST)
                if password_form.is_valid():
                    password_form.save()
                    res_json = {'result': True, "mensaje": "Contraseña Cambiada con exito"}
                    return JsonResponse(res_json, safe=False)
                res_json = {'result': False, "mensaje": "Error en el formulario: {}".format(
                    [{k: v[0]} for k, v in password_form.errors.items()])}
                return JsonResponse(res_json, safe=False)
            except Exception as ex:
                transaction.set_rollback(True)
                res_json = {'result': True, "mensaje": "Error: {}".format(ex)}
            return JsonResponse(res_json, safe=False)


         

        return JsonResponse({"result": "bad", "mensaje": u"Solicitud Incorrecta."})
    else:
        if 'action' in request.GET:
            action = request.GET['action']


        else:
            try:
                data['title'] = 'Ajustes'
                data['title1'] = 'Perfil'
                data['item'] = item = Persona.objects.get(usuario_id=usuario['id'])
                initial = model_to_dict(item)
                initial.update(model_to_dict(item.usuario))
                form = PersonaForm(initial=initial)
                form.quitar()
                password_form = CustomPasswordChangeForm(user=item.usuario)
                data['form'] = form
                data['password_form'] = password_form
                return render(request, "ajustes/view.html", data)
            except Exception as ex:
                pass