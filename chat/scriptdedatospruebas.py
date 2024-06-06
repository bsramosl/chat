import os
import random

import django
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')
# Configura las configuraciones de Django y llama a django.setup()
django.setup()

from django.contrib.auth.models import User
from chat.models import UnidadEducativa, Persona, Parentesco, Curso, Materia, Matricula, Nota
usuarios_creados = set()
unidades_educativas_creadas = set()
fake = Faker()

# Crear Unidades Educativas
unidades_educativas = []
for _ in range(10):
    nombre_unidad = fake.company()
    if nombre_unidad not in unidades_educativas_creadas:
        unidad = UnidadEducativa(
            nombre=nombre_unidad,
            direccion=fake.address(),
            telefono=fake.phone_number()[:10]
        )
        unidad.save()
        unidades_educativas.append(unidad)
        unidades_educativas_creadas.add(nombre_unidad)

# Crear Usuarios y Personas
personas = []
for _ in range(300):
    username = fake.user_name()[:8]
    if username not in usuarios_creados:
        user = User.objects.create_user(
            username=username,
            email=fake.email(),
            password='password123'
        )
        usuarios_creados.add(username)

        persona = Persona(
            nombre=fake.first_name(),
            apellidos=fake.last_name(),
            cedula=fake.ssn()[:10],
            nacimiento=fake.date_of_birth(minimum_age=5, maximum_age=90),
            sexo=random.choice(['1', '2']),
            telefono=fake.phone_number()[:10],
            email=user.email,
            usuario=user,
            unidad_educativa=random.choice(unidades_educativas),
            tipo=random.choice(['Alumno', 'Padre', 'Profesor'])
        )
        persona.save()
        personas.append(persona)

# Crear Parentescos (padres e hijos)
alumnos = [persona for persona in personas if persona.tipo == 'Alumno']
padres = [persona for persona in personas if persona.tipo == 'Padre']
for _ in range(100):
    padre = random.choice(padres)
    hijo = random.choice(alumnos)
    parentesco = Parentesco(
        padre=padre,
        hijo=hijo
    )
    parentesco.save()

# Crear Cursos
profesores = [persona for persona in personas if persona.tipo == 'Profesor']
cursos = []
for _ in range(20):
    curso = Curso(
        nombre=fake.bs(),
        unidad_educativa=random.choice(unidades_educativas),
        profesor=random.choice(profesores)
    )
    curso.save()
    cursos.append(curso)

# Crear Materias
materias = []
for _ in range(20):
    materia = Materia(
        nombre=fake.word()
    )
    materia.save()
    materias.append(materia)

# Crear Matrículas
for _ in range(200):
    matricula = Matricula(
        alumno=random.choice(alumnos),
        curso=random.choice(cursos),
        ano_academico=random.randint(2000, 2024)
    )
    matricula.save()

# Crear Notas
for _ in range(500):
    nota = Nota(
        alumno=random.choice(alumnos),
        curso=random.choice(cursos),
        materia=random.choice(materias),
        nota=random.uniform(0, 10)
    )
    nota.save()

print("Datos de prueba generados exitosamente.")