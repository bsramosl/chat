from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db import models

from django.db import models
from django.contrib.auth.models import User


class UnidadEducativa(models.Model):
    nombre = models.CharField(max_length=100,null=True, blank=True)
    direccion = models.CharField(max_length=200,null=True, blank=True)
    telefono = models.CharField(max_length=20,null=True, blank=True)

    class Meta:
        verbose_name_plural = "Unidades Educativas"

    def __str__(self):
        return self.nombre
class Alumno(models.Model):
    nombre = models.CharField(max_length=100,null=True,blank=True)
    apellidos = models.CharField(max_length=100,null=True,blank=True)
    cedula = models.CharField(max_length=20,null=True,blank=True)
    nacimiento = models.DateField(verbose_name=u"Fecha de nacimiento", null=True, blank=True)
    sexo = models.CharField(max_length=1,null=True,blank=True)
    telefono = models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(default='', max_length=200, verbose_name=u"Correo electronico personal")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    unidad_educativa = models.ForeignKey(UnidadEducativa, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Padre(models.Model):
    nombre = models.CharField(max_length=100,null=True,blank=True)
    apellidos = models.CharField(max_length=100,null=True,blank=True)
    cedula = models.CharField(max_length=20,null=True,blank=True)
    nacimiento = models.DateField(verbose_name=u"Fecha de nacimiento", null=True, blank=True)
    sexo = models.CharField(max_length=1,null=True, blank=True)
    telefono = models.CharField(max_length=20,null=True, blank=True)
    email = models.EmailField(default='', max_length=200, verbose_name=u"Correo electronico personal")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    unidad_educativa = models.ForeignKey(UnidadEducativa, on_delete=models.CASCADE,verbose_name=u'Unidad Educativa',)
    alumno = models.ForeignKey(Alumno,on_delete=models.CASCADE,verbose_name=u'Hijo',null=True, blank=True)

    class Meta:
        verbose_name = "Padre"
        verbose_name_plural = "Padres"

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Profesor(models.Model):
    nombre = models.CharField(max_length=100,null=True,blank=True)
    apellidos = models.CharField(max_length=100,null=True,blank=True)
    cedula = models.CharField(max_length=20,null=True,blank=True)
    nacimiento = models.DateField(verbose_name=u"Fecha de nacimiento", null=True, blank=True)
    sexo = models.CharField(max_length=1,null=True, blank=True)
    telefono = models.CharField(max_length=20,null=True, blank=True)
    email = models.EmailField(default='', max_length=200, verbose_name=u"Correo electronico personal")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    unidad_educativa = models.ForeignKey(UnidadEducativa, on_delete=models.CASCADE,null=True, blank=True)

    class Meta:
        verbose_name_plural = "Profesores"

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Curso(models.Model):
    nombre = models.CharField(max_length=100,null=True,blank=True)
    unidadeducativa = models.ForeignKey(UnidadEducativa, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nombre

class Matricula(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    anoacademico = models.IntegerField(blank=True, null=True, verbose_name=u"Año Academico")

    class Meta:
        verbose_name_plural = "Matrículas"

    def __str__(self):
        return f"{self.alumno} - {self.curso} - {self.anoacademico}"

class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fechainscripcion = models.DateField(verbose_name=u"Fecha de nacimiento", null=True, blank=True)
    periodo = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        verbose_name_plural = "Inscripciones"

    def __str__(self):
        return f"{self.alumno} - {self.curso} - {self.fechainscripcion}"

class Materia(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Materias"

class Nota(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nota = models.FloatField()

    class Meta:
        verbose_name_plural = "Notas"

    def __str__(self):
        return f"{self.alumno} - {self.curso} - {self.materia}"



    def __str__(self):
        return self.nombre