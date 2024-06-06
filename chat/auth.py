from django.db import transaction
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
            if action == 'login':
                try:
                    user = authenticate(username=request.POST['usuario'], password=request.POST['clave'])
                    if user is not None:
                        if not user.is_active:
                            log(u'Login fallido, usuario inactivo: %s' % (request.POST['usuario']), request, "add")
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
                            if user.is_superuser:
                                usuario_data['tipo'] = 'Administrador'
                            else:
                                per = Persona.objects.filter(usuario=user)
                                usuario_data['tipo'] = per.tipo

                            request.session['usuario'] = usuario_data

                            return HttpResponse(json.dumps({"result": "ok","sessionid": request.session.session_key}), content_type="application/json")
                    #log(u'Login fallido, no existe el usuario: %s' % (request.POST['usuario']), request, "add")
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

