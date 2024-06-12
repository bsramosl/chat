# coding=utf-8
from __future__ import division

import re
import sys
from datetime import timedelta, date, time
from operator import itemgetter
import os
import json
import io as StringIO

from django.db import models, connection, connections
from django.contrib.admin.models import LogEntry, ADDITION, DELETION, CHANGE
from django.contrib.auth.models import User, Group, _user_has_perm
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Func, Q, Avg, F,Count

import unicodedata
import socket
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime


unicode = str

def actualizar_instancia_con_form(instancia, formulario):
    """
    Actualiza los campos de la instancia del modelo con los datos del formulario.
    """
    # Obtener el valor actual del campo 'tipo' en la instancia del modelo
    tipo_instancia = getattr(instancia, 'tipo', None)

    for field in formulario.cleaned_data:
        if field == 'hijos':  # Manejar campo many-to-many
            getattr(instancia, field).set(formulario.cleaned_data[field])
        else:
            setattr(instancia, field, formulario.cleaned_data[field])
    if tipo_instancia:
        instancia.tipo = tipo_instancia

    instancia.save()


def convertir_fecha(s):
    if ':' in s:
        sep = ':'
    elif '-' in s:
        sep = '-'
    else:
        sep = '/'

    return date(int(s.split(sep)[2]), int(s.split(sep)[1]), int(s.split(sep)[0]))


def convertir_hora(s):
    if ':' in s:
        sep = ':'
    return time(int(s.split(sep)[0]), int(s.split(sep)[1]))


def convertir_hora_completa(s):
    if ':' in s:
        sep = ':'
    return time(int(s.split(sep)[0]), int(s.split(sep)[1]), int(s.split(sep)[2]))


def convertir_fecha_invertida(s):
    if ':' in s:
        sep = ':'
    elif '-' in s:
        sep = '-'
    else:
        sep = '/'
    return date(int(s.split(sep)[0]), int(s.split(sep)[1]), int(s.split(sep)[2]))

def convertir_fecha_invertida_hora(s):
    if ':' in s:
        sep = ':'
    elif '-' in s:
        sep = '-'
    else:
        sep = '/'
    return datetime(int(s.split(sep)[0]), int(s.split(sep)[1]), int(s.split(sep)[2]), int(s.split(sep)[3]),
                    int(s.split(sep)[4]))


def convertir_fecha_hora(s):
    fecha = s.split(' ')[0]
    hora = s.split(' ')[1]
    if '/' in fecha:
        sep = ':'
    elif '-' in fecha:
        sep = '-'
    else:
        sep = ':'
    return datetime(int(fecha.split(sep)[2]), int(fecha.split(sep)[1]), int(fecha.split(sep)[0]),
                    int(hora.split(':')[0]), int(hora.split(':')[1]))


def convertir_fecha_hora_invertida(s):
    fecha = s.split(' ')[0]
    hora = s.split(' ')[1]
    if '/' in fecha:
        sep = ':'
    elif '-' in fecha:
        sep = '-'
    else:
        sep = ':'
    return datetime(int(fecha.split(sep)[0]), int(fecha.split(sep)[1]), int(fecha.split(sep)[2]),
                    int(hora.split(':')[0]), int(hora.split(':')[1]))

def round_half_up(n, decimals=0):
    import math
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def calculate_username(persona, variant=1):
    alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    s = persona.nombres.lower().split(' ')
    while '' in s:
        s.remove('')
    if persona.apellido2:
        usernamevariant = s[0][0] + persona.apellido1.lower() + persona.apellido2.lower()[0]
    else:
        usernamevariant = s[0][0] + persona.apellido1.lower()
    usernamevariant = usernamevariant.replace(' ', '').replace(u'ñ', 'n').replace(u'á', 'a').replace(u'é', 'e').replace(
        u'í', 'i').replace(u'ó', 'o').replace(u'ú', 'u')
    usernamevariantfinal = ''
    for letra in usernamevariant:
        if letra in alfabeto:
            usernamevariantfinal += letra
    if variant > 1:
        usernamevariantfinal += str(variant)

    if not User.objects.filter(username=usernamevariantfinal).exclude(persona=persona).exists():
        return usernamevariantfinal
    else:
        return calculate_username(persona, variant + 1)

def convertirfecha(fecha):
    try:
        return date(int(fecha[6:10]), int(fecha[3:5]), int(fecha[0:2]))
    except Exception as ex:
        return datetime.now().date()

def convertirfechahora(fecha):
    try:
        return datetime(int(fecha[0:4]), int(fecha[5:7]), int(fecha[8:10]), int(fecha[11:13]), int(fecha[14:16]),
                        int(fecha[17:19]))
    except Exception as ex:
        return datetime.now()

def convertirfechahorainvertida(fecha):
    try:
        return datetime(int(fecha[6:10]), int(fecha[3:5]), int(fecha[0:2]), int(fecha[11:13]), int(fecha[14:16]),
                        int(fecha[17:19]))
    except Exception as ex:
        return datetime.now()


