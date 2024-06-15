from django.contrib import messages
from django.db import transaction
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import get_template

from chat.funciones import *
from chat.forms import *
from django.contrib.auth.models import User, Group
from chat.models import *

@transaction.atomic()
def login_user(request):
    data = {}
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'agregar':
                try:
                    form = PersonaForm(request.POST)
                    if form.is_valid():
                        user = User.objects.create_user(
                            (form.cleaned_data['nombre'].split()[0] + form.cleaned_data['apellidos'].split()[0]),
                            form.cleaned_data['email'],
                            form.cleaned_data['cedula'],
                            first_name=form.cleaned_data['nombre'],
                            last_name=form.cleaned_data['apellidos'])
                        user.save()
                        item = Persona(nombre=form.cleaned_data['nombre'],
                                       apellidos=form.cleaned_data['apellidos'],
                                       cedula=form.cleaned_data['cedula'],
                                       nacimiento=form.cleaned_data['nacimiento'],
                                       telefono=form.cleaned_data['telefono'],
                                       email=form.cleaned_data['email'],
                                       usuario=user,
                                       tipo='Padre')
                        item.save()
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

            if action == 'login':
                try:
                    user = authenticate(username=request.POST['usuario'], password=request.POST['clave'])
                    if user is not None:
                        if not user.is_active:
                            return HttpResponse(
                                json.dumps({"result": "bad", "mensaje": 'Login fallido, usuario inactivo.'}),
                                content_type="application/json")
                        else:
                            login(request, user)
                            request.session['autenticado'] = True
                            usuario_data = {
                                'id': user.id,
                                'username': user.username,
                            }
                            per = Persona.objects.get(usuario=user)
                            usuario_data['tipo'] = per.tipo
                            request.session['usuario'] = usuario_data

                            return HttpResponse(json.dumps({"result": "ok","sessionid": request.session.session_key}), content_type="application/json")
                    return HttpResponse(
                        json.dumps({"result": "bad", "mensaje": 'Login fallido, usuario o clave incorrecta.'}),
                        content_type="application/json")
                except Exception as ex:
                    print("Error durante el proceso de inicio de sesión:", str(ex))
                    return HttpResponse(
                        json.dumps({"result": "bad", "mensaje": 'Login fallido, Error en el sistema. '}),
                        content_type="application/json")

        return HttpResponse(json.dumps({"result": "bad", "mensaje": "Solicitud Incorrecta."}),
                            content_type="application/json")
    else:
        if 'action' in request.GET:
            action = request.GET['action']

            if action == 'registro':
                try:
                    data['action'] = 'agregar'
                    form = PadreForm()
                    form.registro()
                    data['form'] = form
                    template = get_template("padre/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

        if 'autenticado' in request.session:
            return HttpResponseRedirect("/")
        data['request'] = request
        return render(request, "login.html", data)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/login")


@login_required(redirect_field_name='ret', login_url='/login')
@transaction.atomic()
def panel(request):
    data = {}
    data['hoy'] = datetime.now()
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

        return HttpResponse(json.dumps({"result": "bad", "mensaje": 'Solicitud Incorrecta.'}),
                            content_type="application/json")
    else:
        hoy = datetime.now()
        data['title'] = 'Menú Principal'
        if 'action' in request.GET:
            action = request.GET['action']
            return HttpResponseRedirect(request.path)
        else:
            try:
                data['titulo'] = 'Menú Principal'
                data['usuario'] = usuario = request.session['usuario']
                return render(request, "index.html", data)
            except Exception as ex:
                return HttpResponseRedirect('/logout')

