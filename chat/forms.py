from datetime import datetime

from django.forms import DateTimeInput
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User

from .models import *


class UnidadEducativaForm(forms.ModelForm):
    class Meta:
        model = UnidadEducativa
        fields = ['nombre', 'direccion','telefono']


class AlumnoForm(forms.Form):
    nombre = forms.CharField(label=u"Nombres", max_length=400, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'col': '12'}))
    apellidos = forms.CharField(label=u"Apellidos", max_length=400, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'col': '12'}))
    cedula = forms.CharField(max_length=200, label=u'Identificación', required=False,
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'col': '4'}))
    nacimiento = forms.DateField(label=u"Fecha nacimiento", initial=datetime.now().date(),
                                 required=False, input_formats=['%Y-%m-%d'],
                                 widget=DateTimeInput(format='%Y-%m-%d',
                                                      attrs={'class': 'form-control', 'col': '4', 'type': 'date'}))
    sexo = forms.CharField(max_length=200, label=u'Sexo', required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'col': '6'}))
    telefono = forms.CharField(initial=0, required=False, label=u'Telefono.',
                              widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'col': '6', }))
    email = forms.CharField(max_length=200, label=u'Email', required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'col': '6'}))
    unidad_educativa = forms.ModelChoiceField(UnidadEducativa.objects.all(), required=False,
                                       label=u'Unidad Educativa',
                                       widget=forms.Select(attrs={'col': '4'}))



class PadreForm(forms.Form):
    nombre = forms.CharField(label=u"Nombres", max_length=400, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'col': '12'}))
    apellidos = forms.CharField(label=u"Apellidos", max_length=400, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'col': '12'}))
    cedula = forms.CharField(max_length=200, label=u'Identificación', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'col': '4'}))
    nacimiento = forms.DateField(label=u"Fecha nacimiento", initial=datetime.now().date(),
                                 required=False, input_formats=['%Y-%m-%d'],
                                 widget=DateTimeInput(format='%Y-%m-%d',
                                                      attrs={'class': 'form-control', 'col': '4', 'type': 'date'}))
    sexo = forms.CharField(max_length=200, label=u'Sexo', required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'col': '6'}))
    telefono = forms.CharField(initial=0, required=False, label=u'Telefono.',
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'col': '6', }))
    email = forms.CharField(max_length=200, label=u'Email', required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'col': '6'}))
    unidad_educativa = forms.ModelChoiceField(UnidadEducativa.objects.all(), required=False,
                                              label=u'Unidad Educativa',
                                              widget=forms.Select(attrs={'col': '4'}))
    alumno = forms.ModelChoiceField(Alumno.objects.all(), required=False,
                                              label=u'Hijo(s)',
                                              widget=forms.Select(attrs={'col': '4'}))


class MatriculaForm(forms.Form):
    alumno = forms.ModelChoiceField(Alumno.objects.all(), required=False,
                                    label=u'Alumno',
                                    widget=forms.Select(attrs={'col': '4'}))
    curso = forms.ModelChoiceField(Curso.objects.all(), required=False,
                                    label=u'Curso',
                                    widget=forms.Select(attrs={'col': '4'}))
    anoacademico = forms.CharField(label=u"Año academico", max_length=400, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'col': '12'}))


class InscripcionForm(forms.Form):
    alumno = forms.ModelChoiceField(Alumno.objects.all(), required=False,
                                    label=u'Alumno',
                                    widget=forms.Select(attrs={'col': '4'}))
    curso = forms.ModelChoiceField(Curso.objects.all(), required=False,
                                   label=u'Curso',
                                   widget=forms.Select(attrs={'col': '4'}))
    fechainscripcion = forms.CharField(required=False,
                                   label=u'FechaInscripcion',
                                   widget=forms.DateInput(attrs={'col': '4'}))
    perioido = forms.CharField(label=u"Periodo", max_length=400, required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'col': '12'}))


class CursoForm(forms.Form):
    nombre = forms.CharField(label=u"Nombre", max_length=400, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'col': '12'}))
    unidadeducativa = forms.ModelChoiceField(UnidadEducativa.objects.all(), required=False,
                                   label=u'Unidad Educativa',
                                   widget=forms.Select(attrs={'col': '4'}))
    profesor = forms.ModelChoiceField(Profesor.objects.all(), required=False,
                                   label=u'Profesor',
                                   widget=forms.Select(attrs={'col': '4'}))
    class Meta:
        model = Curso
        fields = ['nombre', 'unidadeducativa', 'profesor']


class ProfesorForm(forms.Form):
    nombre = forms.CharField(label=u"Nombres", max_length=400, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'col': '12'}))
    apellidos = forms.CharField(label=u"Apellidos", max_length=400, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'col': '12'}))
    cedula = forms.CharField(max_length=200, label=u'Identificación', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'col': '4'}))
    nacimiento = forms.DateField(label=u"Fecha nacimiento", initial=datetime.now().date(),
                                 required=False, input_formats=['%Y-%m-%d'],
                                 widget=DateTimeInput(format='%Y-%m-%d',
                                                      attrs={'class': 'form-control', 'col': '4', 'type': 'date'}))
    sexo = forms.CharField(max_length=200, label=u'Sexo', required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'col': '6'}))
    telefono = forms.CharField(initial=0, required=False, label=u'Telefono.',
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'col': '6', }))
    email = forms.CharField(max_length=200, label=u'Email', required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'col': '6'}))
    unidad_educativa = forms.ModelChoiceField(UnidadEducativa.objects.all(), required=False,
                                              label=u'Unidad Educativa',
                                              widget=forms.Select(attrs={'col': '4'}))


class NotaForm(forms.Form):
    alumno = forms.ModelChoiceField(Alumno.objects.all(), required=False,
                                   label=u'Alumno',
                                   widget=forms.Select(attrs={'col': '4'}))
    curso = forms.ModelChoiceField(Curso.objects.all(), required=False,
                                   label=u'Curso',
                                   widget=forms.Select(attrs={'col': '4'}))
    materia = forms.ModelChoiceField(Materia.objects.all(), required=False,
                                   label=u'Materia',
                                   widget=forms.Select(attrs={'col': '4'}))
    nota = forms.IntegerField(label=u"Nota",required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'col': '12'}))


class MateriaForm(forms.Form):
    nombre = forms.CharField(max_length=200, label=u'Nombre', required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'col': '6'}))

