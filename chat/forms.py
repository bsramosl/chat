from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import DateTimeInput
from datetime import datetime

from .models import UnidadEducativa, Persona, Curso, Materia, Nota, Matricula


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Contraseña antigua', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UnidadEducativaForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(label="Dirección", max_length=200, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label="Teléfono", max_length=20, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))


class PersonaForm(forms.Form):
    SEXO_CHOICES = [
        ('1', 'Masculino'),
        ('2', 'Femenino'),
    ]
    nombre = forms.CharField(label="Nombre", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellidos = forms.CharField(label="Apellidos", max_length=100, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    cedula = forms.CharField(label="Cédula", max_length=20, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    nacimiento = forms.DateField(label="Fecha de Nacimiento", initial=datetime.now().date(), required=False,
                                 input_formats=['%Y-%m-%d'],
                                 widget=DateTimeInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    sexo = forms.ChoiceField(label="Sexo", choices=SEXO_CHOICES, required=False,
                             widget=forms.Select(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label="Teléfono", max_length=20, required=False,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo Electrónico", max_length=200, required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    unidad_educativa = forms.ModelChoiceField(queryset=UnidadEducativa.objects.all(), required=False,
                                              label="Unidad Educativa",
                                              widget=forms.Select(attrs={'class': 'form-control'}))
    tipo = forms.ChoiceField(choices=[('alumno', 'Alumno'), ('padre', 'Padre'), ('profesor', 'Profesor')],
                             required=False, label="Tipo", widget=forms.HiddenInput())

    def quitar(self):
        del self.fields['tipo']


    def registro(self):
        del self.fields['sexo']
        del self.fields['tipo']
        del self.fields['unidad_educativa']
        del self.fields['hijos']


class AlumnoForm(PersonaForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo'].initial = 'alumno'
        self.fields['tipo'].widget = forms.HiddenInput()


class PadreForm(PersonaForm):
    hijos = forms.ModelMultipleChoiceField(queryset=Persona.objects.filter(tipo='Alumno'), required=False,
                                           label="Hijo(s)",
                                           widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo'].initial = 'padre'
        self.fields['tipo'].widget = forms.HiddenInput()


class ProfesorForm(PersonaForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo'].initial = 'profesor'
        self.fields['tipo'].widget = forms.HiddenInput()


class MatriculaForm(forms.Form):
    alumno = forms.ModelChoiceField(queryset=Persona.objects.filter(tipo='Alumno'), required=False, label="Alumno",
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(), required=False, label="Curso",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    ano_academico = forms.CharField(label="Año Académico", max_length=4, required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))



class CursoForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    unidad_educativa = forms.ModelChoiceField(queryset=UnidadEducativa.objects.all(), required=False, label="Unidad Educativa",
                                              widget=forms.Select(attrs={'class': 'form-control'}))
    profesor = forms.ModelChoiceField(queryset=Persona.objects.filter(tipo='Profesor'), required=False, label="Profesor",
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    materia = forms.ModelMultipleChoiceField(queryset=Materia.objects.all(), required=False,
                                           label="Materia",
                                           widget=forms.SelectMultiple(attrs={'class': 'form-control'}))


class NotaForm(forms.Form):
    alumno = forms.ModelChoiceField(queryset=Persona.objects.filter(tipo='Alumno'), required=False, label="Alumno",
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    materia = forms.ModelChoiceField(queryset=Materia.objects.all(), required=False, label="Materia",
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    nota = forms.FloatField(label="Nota", required=False,
                            widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def quitar(self):
        deshabilitar_campo(self, 'materia')
        deshabilitar_campo(self, 'alumno')




class MateriaForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(), required=False, label="Curso",
                                   widget=forms.Select(attrs={'class': 'form-control'}))


def deshabilitar_campo(form, campo):
    form.fields[campo].widget.attrs['readonly'] = True
    form.fields[campo].widget.attrs['disabled'] = True


def habilitar_campo(form, campo):
    form.fields[campo].widget.attrs['readonly'] = False
    form.fields[campo].widget.attrs['disabled'] = False


def campo_solo_lectura(form, campo):
    form.fields[campo].widget.attrs['readonly'] = True