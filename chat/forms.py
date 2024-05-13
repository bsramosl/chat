from django.utils import timezone
from django import forms
from django.contrib.auth.models import User

from .models import *


class UnidadEducativaForm(forms.ModelForm):
    class Meta:
        model = UnidadEducativa
        fields = ['nombre', 'direccion','telefono']


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['usuario', 'unidades_educativas']


class PadreForm(forms.ModelForm):
    class Meta:
        model = Padre
        fields = ['usuario', 'hijos']


class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ['alumno', 'curso', 'año_academico']

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['alumno', 'curso', 'periodo']



class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'unidad_educativa', 'profesor']


class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['usuario', 'unidades_educativas']


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['alumno', 'curso', 'materia', 'nota']


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['nombre']