from chat import auth,settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from chat.views import *
from chat import unidadeducativa , alumno , padre, matricula, nota,curso,materia ,profesor,ajustes,perfil

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',auth.panel,name="principal"),
    path('login', auth.login_user, name='Loginuser'),
    path('logout', auth.logout_user, name='Logout'),
    path('unidadeducativa', unidadeducativa.view, name='unidadeducativa'),
    path('alumno', alumno.view, name='alumno'),
    path('padre', padre.view, name='padre'),
    path('profesor', profesor.view, name='profesor'),
    path('matricula', matricula.view, name='matricula'),
    path('nota', nota.view, name='nota'),
    path('curso', curso.view, name='curso'),
    path('materia', materia.view, name='materia'),
    path('send_message', send_message, name='send_message'),

    path('ajustes', ajustes.view, name='ajustes'),
    path('perfil', perfil.view, name='perfil'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)