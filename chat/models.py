from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db import models

from django.db import models
from django.contrib.auth.models import User

class UnidadEducativa(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)

    def _str_(self):
        return self.nombre

class Alumno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    unidades_educativas = models.ManyToManyField(UnidadEducativa, related_name='alumnos')

    def __str__(self):
        return u'%s' % (self.usuario)

    class Meta:
        verbose_name = u"Alumno"
        verbose_name_plural = u"Alumnos"

class Padre(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    hijos = models.ManyToManyField(Alumno, related_name='padres')

    def __str__(self):
        return u'%s' % (self.usuario)

    class Meta:
        verbose_name = u"Padre"
        verbose_name_plural = u"Padres"


class Matricula(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    año_academico = models.PositiveIntegerField()

    def _str_(self):
        return f"{self.alumno} - {self.curso} - {self.año_academico}"

    class Meta:
        verbose_name = u"Matricula"
        verbose_name_plural = u"Matriculas"

class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    periodo = models.CharField(max_length=50)  # Agregar el periodo de inscripción

    def _str_(self):
        return f"{self.alumno} - {self.curso} ({self.periodo})"

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    unidad_educativa = models.ForeignKey(UnidadEducativa, on_delete=models.CASCADE)
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE)

    def _str_(self):
        return self.nombre

class Profesor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    unidades_educativas = models.ManyToManyField(UnidadEducativa, related_name='profesores')

    def _str_(self):
        return self.usuario.username

class Nota(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2)

    def _str_(self):
        return f"{self.alumno} - {self.materia}: {self.nota}"

class Materia(models.Model):
    nombre = models.CharField(max_length=100)

    def _str_(self):
        return self.nombre
