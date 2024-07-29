import os
import random
import django
from faker import Faker

fake = Faker('es_ES')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')
django.setup()
from chat.views import verificar_cedula

from django.contrib.auth.models import User
from chat.models import UnidadEducativa, Persona, Parentesco, Curso, Materia, Matricula, Nota

usuarios_creados = set()
unidades_educativas_creadas = set()

UnidadEducativa.objects.all().delete()
Persona.objects.all().delete()
Parentesco.objects.all().delete()
Curso.objects.all().delete()
Materia.objects.all().delete()
Matricula.objects.all().delete()
Nota.objects.all().delete()
User.objects.all().delete()

def generar_cedula_valida():
    # Generar los primeros dos dígitos que representan la provincia
    provincia = random.randint(1, 24)
    digitos = [provincia // 10, provincia % 10]  # ester es mayor a 6
    # Generar los siguientes seis dígitos aleatorios
    digitos += [random.randint(0, 9) for _ in range(7)]
    # Coeficientes para el cálculo del dígito verificador
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]  # para todos menos el ultimo digito luego se calcula
    # Calcular la suma según los coeficientes
    suma = 0
    for d, c in zip(digitos, coeficientes):
        producto = d * c
        if producto >= 10:
            producto -= 9
        suma += producto
    # Calcular el dígito verificador -->>este es el ultimo digito de la suma de arriba
    digito_verificador = (10 - suma % 10) % 10
    # Añadir el dígito verificador a la lista de dígitos
    digitos.append(digito_verificador)
    # Convertir la lista de dígitos en una cadena de texto
    cedula = ''.join(map(str, digitos))
    return cedula



admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password123')
persona = Persona(
    nombre='admin',
    apellidos='admin',
    cedula=generar_cedula_valida(),
    nacimiento=fake.date_of_birth(minimum_age=5, maximum_age=90),
    sexo=random.choice(['1', '2']),
    telefono=fake.phone_number()[:10],
    email='admin@example.com',
    usuario=admin_user,
    tipo='Administrador'
)
persona.save()

if not admin_user.is_superuser:
    admin_user.is_superuser = True
    admin_user.save()

# Crear Unidades Educativas
unidades_educativas = []
for _ in range(1):
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
        cedula = generar_cedula_valida()
        if verificar_cedula(cedula):
            persona = Persona(
                nombre=fake.first_name(),
                apellidos=fake.last_name(),
                cedula=cedula,
                nacimiento=fake.date_of_birth(minimum_age=5, maximum_age=90),
                sexo=random.choice(['1', '2']),
                telefono=fake.phone_number()[:10],
                email=user.email,
                usuario=user,
                unidad_educativa=unidades_educativas[0],
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

# Crear cursos específicos
profesores = [persona for persona in personas if persona.tipo == 'Profesor']
# Lista de nombres de cursos específicos
nombres_cursos = [
    "Inicial 1", "Inicial 2", "Pre - Escolar", "Primer Grado", "Segundo Grado",
    "Tercer Grado", "Cuarto Grado", "Quinto Grado", "Sexto Grado", "Septimo Grado",
    "Octavo Grado", "Noveno Grado", "Decimo Grado",
    "Primero de bachillerato Tecnico", "Segundo de bachillerato Tecnico",
    "Tercero de bachillerato Tecnico", "Primero de bachillerato Ciencias",
    "Segundo de bachillerato Ciencias", "Tercero de bachillerato Ciencias"
]

cursos = []
for nombre in nombres_cursos:
    curso = Curso(
        nombre=nombre.lower(),
        unidad_educativa=unidades_educativas[0],
        profesor=random.choice(profesores)
    )
    curso.save()
    cursos.append(curso)

# Crear Materias
materias = []
for _ in range(40):
    materia = Materia(
        nombre=fake.word(),
        curso = random.choice(cursos),
    )
    materia.save()
    materias.append(materia)

# Crear Matrículas
for _ in range(100):
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
        materia=random.choice(materias),
        nota=random.uniform(0, 10)
    )
    nota.save()

print("Datos de prueba generados exitosamente.")