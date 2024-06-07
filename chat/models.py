from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.shortcuts import get_object_or_404


class UnidadEducativa(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Unidades Educativas"

    def __str__(self):
        return self.nombre

class Persona(models.Model):
    TIPOS_PERSONA = (
        ('alumno', 'Alumno'),
        ('padre', 'Padre'),
        ('profesor', 'Profesor'),
    )

    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellidos = models.CharField(max_length=100, null=True, blank=True)
    cedula = models.CharField(max_length=20, null=True, blank=True)
    nacimiento = models.DateField(verbose_name="Fecha de nacimiento", null=True, blank=True)
    sexo = models.CharField(max_length=1, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(default='', max_length=200, verbose_name="Correo electrónico personal")
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    unidad_educativa = models.ForeignKey(UnidadEducativa, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPOS_PERSONA)

    class Meta:
        verbose_name_plural = "Personas"

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Parentesco(models.Model):
    padre = models.ForeignKey(Persona, related_name='hijos', on_delete=models.CASCADE)
    hijo = models.ForeignKey(Persona, related_name='padres', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.padre} -> {self.hijo}"


class Curso(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    unidad_educativa = models.ForeignKey(UnidadEducativa, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Persona, on_delete=models.CASCADE, limit_choices_to={'tipo': 'profesor'})


    class Meta:
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nombre

class Matricula(models.Model):
    alumno = models.ForeignKey(Persona, on_delete=models.CASCADE, limit_choices_to={'tipo': 'alumno'})
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    ano_academico = models.IntegerField(blank=True, null=True, verbose_name="Año Académico")

    class Meta:
        verbose_name_plural = "Matrículas"

    def __str__(self):
        return f"{self.alumno} - {self.curso} - {self.ano_academico}"



class Materia(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Materias"

    def __str__(self):
        return f"{self.nombre} "

class Nota(models.Model):
    alumno = models.ForeignKey(Persona, on_delete=models.CASCADE, limit_choices_to={'tipo': 'alumno'})
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)  # Agregar clave externa a Curso
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nota = models.FloatField()

    class Meta:
        verbose_name_plural = "Notas"

    def __str__(self):
        return f"{self.alumno} - {self.curso} - {self.materia}"

def obtener_materias_y_notas_por_curso(curso_id):
    curso = Curso.objects.filter(pk=curso_id)
    materias = Nota.objects.filter(curso_id=curso_id).annotate(total_alumnos=Count('alumno', distinct=True))
    return materias