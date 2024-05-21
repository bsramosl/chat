from chat import auth

from django.contrib import admin
from django.urls import path
from chat.views import *
from chat import unidadeducativa , alumno , padre, matricula, inscripcion,nota,curso,materia

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',auth.panel,name="principal"),
    path('login', auth.login_user, name='Loginuser'),
    path('logout', auth.logout_user, name='Logout'),
    path('registro', auth.registrar_padre, name='registro'),
    path('unidadeducativa', unidadeducativa.view, name='unidadeducativa'),
    path('alumno', alumno.view, name='alumno'),
    path('padre', padre.view, name='padre'),
    path('matricula', matricula.view, name='matricula'),
    path('inscripcion', inscripcion.view, name='inscripcion'),
    path('nota', nota.view, name='nota'),
    path('curso', curso.view, name='curso'),
    path('materia', materia.view, name='materia'),
]
