
from django.contrib.auth.models import User
from django.shortcuts import *
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import spacy
from chat.auth import auth
from chat.models import Persona, Nota, Curso, Parentesco, Materia
from django.middleware.csrf import get_token
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
nlp = spacy.load('es_core_news_md')

usuario = None

registro_en_proceso = False
login_en_proceso = False
mis_materiasb = False
mis_cursosb = False
registrar_hijob = False
notas_hijob = False
profesores_hijob = False
contacto_docenteb = False
mis_estudiantesb = False
contacto_docente_materia_b = False



cambio_contrasena_en_proceso = False
mis_notas_alumno = False
registro_materia = False
mis_profesoresb = False


nombre = ""
apellido = ""
fecha_nacimiento = ""
cedula = ""
email = ""
personalisada = ""
curso=""
materia=""




def verificar_cedula(cedula):
    total = 0
    tamano_longitud_cedula = 10
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    numero_provincias = 24
    tercer_digito = 6

    if len(cedula) == tamano_longitud_cedula and cedula.isdigit():
        provincia = int(cedula[0:2])
        digito_tres = int(cedula[2])

        if 0 < provincia <= numero_provincias and digito_tres < tercer_digito:
            digito_verificador_recibido = int(cedula[9])
            for i in range(len(coeficientes)):
                valor = int(cedula[i]) * coeficientes[i]
                if valor >= 10:
                    valor -= 9
                total += valor

            digito_verificador_obtenido = 10 - (total % 10) if total % 10 != 0 else 0

            if digito_verificador_obtenido == digito_verificador_recibido:
                return True
    return False


@csrf_exempt
def twilio_webhook(request):
    if request.method == 'POST':
        message_body = request.POST.get('Body', '')
        print(request.POST)

        response_text = generate_response(message_body,request)  # Tu función para generar la respuesta

        resp = MessagingResponse()
        resp.message(response_text)
        return HttpResponse(str(resp), content_type='text/xml')
    return JsonResponse({'error': 'Invalid request'}, status=400)

def Index(request):
    return render(request,'index.html')


@csrf_exempt
def send_message(request):
    global usuario
    if 'usuario' in request.session:
        usuario = request.session['usuario']

    if request.method == 'POST':
        data = json.loads(request.body)
        body = data.get('message')
        try:
            response_text = generate_response(body,request)

            if response_text == "perfil":
                return JsonResponse({'success': True, 'redirect_url': '/perfil'})
            if response_text == "ajustes":
                return JsonResponse({'success': True, 'redirect_url': '/ajustes'})
            return JsonResponse({'success': True, 'message': response_text})
        except Exception as e:
            return JsonResponse({'error': f"Failed to process message: {e}"}, status=500)
    else:
        return JsonResponse({'error': "This endpoint only accepts POST requests."}, status=405)


def generate_response(message,request):
    global registro_en_proceso,login_en_proceso,personalisada

    message = message.lower()
    doc = nlp(message)

    if message == "cancelar" or message == "exit":
        return procesar_salir()

    if message == "salir":
        return procesarpersonalizada(request)

    if contacto_docente_materia_b:
        return procesar_respuesta_contacto_docente_materia(message)

    if mis_estudiantesb:
        return procesar_respuesta_mis_estudiantes(message)

    if contacto_docenteb:
        return procesar_respuesta_contacto_docente(message)

    if  mis_profesoresb:
        return procesar_respuesta_mis_profesores(message)

    if registro_materia:
        return procesar_registro_materias_alumno(message)

    if profesores_hijob:
        return procesar_respuesta_mis_profesores_hijo(message)

    if login_en_proceso:
        return procesar_respuesta_login(message, request)

    if mis_cursosb:
        return procesar_respuesta_mis_cursosb(message)

    if notas_hijob:
        return procesar_respuesta_notas_hijo(message)

    if mis_materiasb:
        return procesar_respuesta_mis_materias(message)

    if mis_notas_alumno:
        return procesar_mis_notas_alumno(message)

    if registrar_hijob:
        return procesar_respuesta_registrarhijo(message)

    if cambio_contrasena_en_proceso:
        return procesar_respuesta_cambio_contrasena(message, request)

    if registro_en_proceso:
        return procesar_respuesta_registro(message)

    if not personalisada:
        if not 'usuario' in request.session:
            if len(message) == 10 and message.isdigit():
                if not verificar_cedula(message):
                    return "Número de cédula incorrecto. Proporciona un número de cédula valido."
                try:
                    personalisada = Persona.objects.get(cedula=message)
                    request.session['tp'] = personalisada.tipo
                    return f"En que puedo ayudarte \n{personalisada.nombre}"
                except Exception as e:
                    return "No existe persona registrada con el numero de cedula ingresado"

    # Si no hay un proceso de registro en curso, procesar como de costumbre
    if not registro_en_proceso:
    
        responses = {
            "login": iniciar_login,
            "iniciar sesion": iniciar_login,
            "logearse": iniciar_login,
            "registro": iniciar_registro,
            "logout": lambda: cerrar_sesion(request),
            "cerrar sesion": lambda: cerrar_sesion(request),
            "mis materias": mis_materias,
            "cuales son las notas de mi hijo": notas_hijo,
            "cuales son los profesores de mi hijo": profesores_hijo,
            "notas de mi hijo": notas_hijo,
            "mis cursos": mis_cursos,
            "perfil": perfil(request),
            "ajustes": ajustes(request),
            "cambio de contraseña": iniciar_cambio_contrasena,
            "cambiar contraseña": iniciar_cambio_contrasena,
            "mis notas": iniciar_misnotas,
            "registrar hijo": registrar_hijo,
            "registrar materias alumno":iniciar_registro_materia_alumno,
            "contacto del docente": contacto_docente,
            "mis profesores": mis_profesores,
            "mis estudiantes": mis_estudiantes,
            "contacto del docente por materia": contacto_docente_materia,

            "hola": "¡Hola! ¿Cómo puedo ayudarte hoy?",
            "adiós": "¡Adiós! Que tengas un buen día.",
            "cómo estás": "Estoy bien, gracias por preguntar. ¿Y tú?",
            "qué puedes hacer": "Puedo responder preguntas básicas. ¿Qué te gustaría saber?",
            "quién eres": "Soy un chatbot creado para ayudarte. ¿En qué puedo asistirte?",
            "gracias": "De nada. ¿Hay algo más en lo que pueda ayudarte?",
            "cómo me puedo registrar": "Para registrarte, puedes iniciar el proceso escribiendo 'registro'.",
            "cuáles son los requisitos": "Los requisitos para registrarse incluyen nombre completo, fecha de nacimiento, correo electrónico y número de cédula.",
            "cómo registro a mi hijo": "Para registrar a tu hijo, por favor proporciona los detalles de su nombre,apellido, fecha de nacimiento, número de identificación y correo.",
            "qué cursos hay": "Actualmente ofrecemos una variedad de cursos. Por favor visita nuestra página web para más detalles.",
            "cuánto cuesta el registro": "El costo del registro varía dependiendo del curso. Por favor, visita nuestra página de tarifas para más detalles.",
            "cuál es su horario de atención": "Nuestro horario de atención es de lunes a viernes, de 9:00 AM a 6:00 PM.",
            "ofrecen cursos en línea": "Sí, ofrecemos una variedad de cursos en línea. Visita nuestra página web para más información.",
            "cuánto duran los cursos": "La duración de los cursos varía. Algunos son de unas pocas semanas, mientras que otros pueden durar varios meses.",
            "qué documentos necesito para el registro": "Necesitas tu identificación oficial, comprobante de domicilio y los documentos específicos del curso que elijas.",
            "cómo puedo contactar con soporte": "Puedes contactar con soporte enviando un correo a soporte@nuestraescuela.com o llamando al (123) 456-7890.",
            "hay descuentos disponibles": "Sí, ofrecemos descuentos para estudiantes, miembros de la misma familia y pagos anticipados.",
            "cómo puedo pagar": "Aceptamos pagos con tarjeta de crédito, débito y transferencias bancarias.",
            "puedo visitar las instalaciones": "Sí, puedes agendar una visita a nuestras instalaciones llamando al (123) 456-7890.",
            "hay plazas disponibles": "La disponibilidad de plazas varía según el curso.",
            "cómo cancelo mi inscripción": "Para cancelar tu inscripción, por favor contacta con nuestro soporte.",
            "hay actividades extracurriculares": "Sí, ofrecemos una variedad de actividades extracurriculares como deportes, artes y clubes académicos.",
            "puedo cambiar de curso": "Sí, puedes solicitar un cambio de curso contactando con soporte.",
            "cómo se evalúa a los estudiantes": "La evaluación de los estudiantes se realiza a través de exámenes, proyectos y participación en clase.",
            "hay becas disponibles": "Sí, ofrecemos becas para estudiantes destacados y aquellos con necesidades financieras.",
            "cuándo comienzan los cursos": "Los cursos comienzan en diferentes fechas a lo largo del año. Consulta nuestra página web para el calendario de inicio.",
            "puedo inscribirme a más de un curso": "Sí, puedes inscribirte a varios cursos, siempre y cuando no haya conflictos de horario.",
            "qué nivel de español necesito": "Nuestros cursos están diseñados para hablantes nativos y avanzados de español. Consulta los requisitos específicos del curso.",
            "tienen estacionamiento": "Sí, nuestras instalaciones cuentan con estacionamiento gratuito para estudiantes.",
            "hay transporte escolar": "Ofrecemos transporte escolar en áreas seleccionadas. Consulta con soporte para más información.",
            "puedo hablar con un instructor": "Sí, puedes agendar una cita para hablar con un instructor contactando con soporte.",
            "qué pasa si tengo una emergencia y no puedo asistir": "En caso de emergencia, notifica a soporte y haremos los arreglos necesarios para que no pierdas contenido importante.",
            "cómo se manejan las ausencias": "Las ausencias deben justificarse a través de soporte. Se permiten un número limitado de ausencias justificadas por curso.",
            "hay tutorías disponibles": "Sí, ofrecemos tutorías personalizadas. Consulta con soporte para más detalles.",
            "cómo accedo a mi cuenta en línea": "Puedes acceder a tu cuenta en línea desde nuestra página web usando tu usuario y contraseña.",

            "inscripción a cursos": "Para inscribirte a cursos, dirígete a la sección de 'Cursos Disponibles' en tu cuenta y selecciona los cursos en los que deseas inscribirte.",
            "materias disponibles": "Puedes ver la lista de materias disponibles en la sección 'Materias' de nuestra página web.",
            "calificaciones": "Las calificaciones de los alumnos pueden ser consultadas en la sección 'Materias' después de iniciar sesión en tu cuenta como docente.",
            "calificaciones de los hijos": "Puedes ver las calificaciones de tus hijos en la sección  una vez que hayas iniciado sesión en tu cuenta.",
            "cursos del docente": "Los cursos que dicta el docente pueden ser vistos en la sección 'Cursos' al iniciar sesión.",
            "cursos del alumno": "Los cursos en los que está inscrito el alumno pueden ser consultados en la sección 'Materias' después de iniciar sesión en tu cuenta.",
            "información del alumno": "La información detallada del alumno está disponible en la sección 'Perfil' una vez que hayas iniciado sesión.",
            # Nuevas respuestas agregadas
            "cómo funciona el proceso de inscripción": "El proceso de inscripción incluye completar el formulario en línea.",
            "dónde puedo encontrar el formulario de inscripción": "El formulario de inscripción está disponible en la sección de 'Registro' de nuestra página web.",
            "necesito ayuda con el formulario de inscripción": "Para recibir ayuda con el formulario de inscripción, puedes contactar con soporte a través de correo o teléfono.",
            "cuál es el proceso de matriculación": "El proceso de matriculación incluye la verificación de documentos, la asignación de cursos.",
            "cómo puedo verificar el estado de mi inscripción": "Puedes verificar el estado de tu inscripción iniciando sesión en tu cuenta y yendo a la sección de mis materias.",
            "qué hacer si tengo problemas con la inscripción en línea": "Si tienes problemas con la inscripción en línea, por favor contacta con soporte para recibir asistencia.",
            "cómo actualizo mis datos personales": "Puedes actualizar tus datos personales iniciando sesión en tu cuenta y accediendo a la sección de 'Perfil'.",
            "qué debo hacer si olvidé mi contraseña": "Si olvidaste tu contraseña, puedes restablecerla utilizando la opción 'Olvidé mi contraseña' en la página de inicio de sesión.",
            "hay penalizaciones por cancelar mi inscripción": "Las penalizaciones por cancelar tu inscripción dependen de la política de cancelación del curso. Por favor, revisa los términos o contacta con soporte.",
            "cómo solicito un reembolso": "Para solicitar un reembolso, por favor contacta con soporte y proporciona los detalles de tu inscripción y la razón de la solicitud.",
            "cómo inscribo a más de un hijo": "Para inscribir a más de un hijo, completa el formulario de inscripción por separado para cada uno y sigue el proceso de pago correspondiente.",
            "hay programas de orientación para nuevos estudiantes": "Sí, ofrecemos programas de orientación para nuevos estudiantes para ayudarles a adaptarse a nuestra institución.",
            "cómo obtengo ayuda financiera para la inscripción": "Para obtener ayuda financiera, puedes aplicar a nuestras becas o planes de financiamiento. Contacta con soporte para más detalles.",
            "hay plazos para la inscripción": "Sí, existen plazos específicos para la inscripción. Por favor, consulta nuestra página web o contacta con soporte para más información."


        }

        best_response = None
        max_similarity = 0

        # Procesar la similitud con las respuestas predefinidas
        for question, response in responses.items():
            question_doc = nlp(question)
            similarity = doc.similarity(question_doc)
            if similarity > max_similarity:  # Umbral de similitud
                max_similarity = similarity
                best_response = response

        if best_response:
            if callable(best_response):
                return best_response()
            else:
                return best_response

        # Si no se encuentra ninguna respuesta predefinida, retornar mensaje de error
        return "Lo siento, no entiendo tu pregunta."
    else:
        # Procesar respuestas durante el registro
        return procesar_respuesta_registro(message)


def iniciar_registro():
    global registro_en_proceso
    registro_en_proceso = True
    return "Para comenzar el registro, por favor proporciona tus nombres:"


def procesar_respuesta_registro(message):
    global registro_en_proceso,nombre,apellido, fecha_nacimiento, cedula,email
    doc = nlp(message)
    if not nombre:
       if not message.isdigit():
           nombre = message
           return "Proporciona tu apellido:"
       return "No pude reconocer tu nombre. Por favor, proporciona tu nombre."
    if not apellido:
        if not message.isdigit():
                apellido = message
                return "Proporciona tu fecha de nacimiento (AAAA-MM-DD):"
        return "No pude reconocer tu apellido. Por favor, proporciona tu apellido."

    if not fecha_nacimiento:
        try:
            fecha =parse_date(message)
            fecha_nacimiento = fecha
            return "Proporciona tu correo electrónico:"
        except ValueError:
            return "Formato de fecha incorrecto. Proporciona tu fecha de nacimiento en el formato AAAA-MM-DD."

    if not email:
        if "@" in message and "." in message:
            email = message
            return "Proporciona tu número de cédula:"
        else:
            return "Correo electrónico inválido. Proporciona un correo electrónico válido."

    if not cedula:
        if len(message) == 10 and message.isdigit():
            if not verificar_cedula(message):
                return "Número de cédula incorrecto. Proporciona un número de cédula valido."
            cedula = message
            return registro()
        else:
            return "Número de cédula incorrecto. Proporciona un número de cédula de 10 dígitos."
    return "Por favor, proporciona la información solicitada."


def registro():
    global registro_en_proceso, nombre, apellido, fecha_nacimiento, cedula ,email
    user = User.objects.create_user((nombre.split()[0] + apellido.split()[0]), email, 'password123',first_name=nombre,
                                                    last_name=apellido)
    user.save()
    item = Persona(nombre=nombre,
                   apellidos=apellido,
                   cedula=cedula,
                   nacimiento=fecha_nacimiento,
                   email=email,
                   usuario=user,
                   tipo='Padre')

    item.save()
    mensaje_confirmacion = (f"Tus datos han sido registrados:\n"
                            f"Nombre: {nombre}\n"
                            f"Apellido: {apellido}\n"
                            f"Fecha de nacimiento: {fecha_nacimiento}\n"
                            f"Cédula: {cedula}")
    procesar_salir()
    return mensaje_confirmacion

def iniciar_login():
    global usuario,login_en_proceso
    if not usuario:
        login_en_proceso = True
        return "Por favor, proporciona tu nombre de usuario para iniciar sesión:"
    return "Estas logeado. Como puedo ayudarte?"


def procesar_respuesta_login(message, request):
    global login_en_proceso

    if 'username' not in request.session:
        request.session['username'] = message
        return "Por favor, proporciona tu contraseña:"

    if 'password' not in request.session:
        request.session['password'] = message
        username = request.session['username']
        password = request.session['password']

        csrf_token = get_token(request)  # Obtener el token CSRF actual
        data = {
            'action': 'login',
            'usuario': username,
            'clave': password,
            'csrfmiddlewaretoken': csrf_token,  # Incluir el token CSRF en los datos
        }


        try:
            sesion = request.session
            request.method = 'POST'
            request.POST = data
            request.META['HTTP_REFERER'] = 'http://127.0.0.1:8000/'  # Establecer el Referer en los headers
            response = auth.login_user(request)
            response_content = response.content.decode('utf-8')  # Convertir bytes a cadena de texto
            # Convertir la cadena JSON a un diccionario Python
            data = json.loads(response_content)
            # Obtener el valor de 'result'
            result_value = data['result']
            if result_value == "ok" :
                procesar_salir()
                del sesion['username']
                del sesion['password']
                return "logueado"
            else:
                del sesion['username']
                del sesion['password']
                return "Login fallido, usuario o clave incorrecta"

        except Exception as e:
            del request.session['username']
            del request.session['password']
            return f"Error en la solicitud de inicio de sesión: {str(e)}"
    return "Por favor, proporciona la información solicitada."

def cerrar_sesion(request):
    global usuario
    try:
        if usuario:
            auth.logout_user(request)
            usuario = None
            return "Sesión cerrada exitosamente"
        return "No esta logueado"
    except Exception as e:
        return f"Error al cerrar sesión: {str(e)}"

def registrar_hijo():
    global registrar_hijob,personalisada,usuario
    registrar_hijob = True
    if personalisada:
        return "Para comenzar el registro, por favor proporciona los nombres:"
    if usuario:
        return "Para comenzar el registro, por favor proporciona los nombres:"
    return "Para iniciar con el registro debe de loguearse o ingresar su numero de cedula"

def notas_hijo():
    global notas_hijob
    notas_hijob = True
    if usuario:
        return procesar_respuesta_notas_hijo(usuario['cedula'])
    return "Para conocer las notas de tu hijo ingresa su numero de cedula:"

def profesores_hijo():
    global profesores_hijob,personalisada
    profesores_hijob = True
    if personalisada:
        return procesar_respuesta_mis_profesores_hijo(personalisada.cedula)
    if usuario:
        return procesar_respuesta_mis_profesores_hijo(usuario['cedula'])
    return "Para conocer los profesores de tu hijo ingresa su numero de cedula:"


def mis_cursos():
    global mis_cursosb,personalisada,usuario
    mis_cursosb = True
    if personalisada:
        return procesar_respuesta_mis_cursosb(personalisada.cedula)
    if usuario:
        return procesar_respuesta_mis_cursosb(usuario['cedula'])
    return "Para conocer tus cursos ingresa tu numero de cedula:"

def mis_materias():
    global mis_materiasb,personalisada,usuario
    mis_materiasb = True
    if personalisada:
        return procesar_respuesta_mis_materias(personalisada.cedula)
    if usuario:
        return procesar_respuesta_mis_materias(usuario['cedula'])
    return "Para conocer tus materias ingresa tu numero de cedula:"

def procesar_respuesta_mis_materias(message):
    global mis_materiasb,cedula
    if message:
        if len(message) == 10 and message.isdigit():
            if not verificar_cedula(message):
                return "Número de cédula incorrecto. Proporciona un número de cédula valido."
            cedula = message
            try:
                persona = Persona.objects.get(cedula=cedula)
                if persona.tipo == 'Profesor':
                    materias = Nota.objects.filter(materia__curso__profesor=persona).values_list('materia__nombre', flat=True).distinct('materia')
                else:
                    materias = Nota.objects.filter(alumno=persona).values_list('materia__nombre', flat=True).distinct()
                if materias:
                    procesar_salir()
                    materias_lista = '\n'.join(f"- {materia}" for materia in materias)
                    if persona.tipo == 'Profesor':
                        return f"Tus Materias son:\n{materias_lista}"
                    return f"Las materias del alumno con cédula {cedula} son:\n{materias_lista}"
                    cedula = ""
                else:
                    cedula = ""
                    return "El alumno no tiene materias registradas."
            except Persona.DoesNotExist:
                return "No se encontró un alumno con la cédula proporcionada."
        else:
            cedula = ""
            return "Número de cédula incorrecto. Proporciona un número de cédula de 10 dígitos."
    return "Por favor, proporciona la información solicitada."

def procesar_respuesta_notas_hijo(message):
    global notas_hijob, cedula,usuario
    if usuario:
        parentesco = Parentesco.objects.filter(padre__cedula=message).first()
        message = parentesco.hijo.cedula if parentesco is not None else None
        if not message:
            notas_hijob = False
            return "No tiene hijos registrados."
    if not cedula:
        if len(message) == 10 and message.isdigit():
            if not verificar_cedula(message):
                return "Número de cédula incorrecto. Proporciona un número de cédula valido."
            cedula = message
            try:
                persona = Persona.objects.get(cedula=cedula)
                notas = Nota.objects.filter(alumno=persona).select_related('materia').distinct()
                if notas:
                    materias_y_notas = '\n'.join(f"- {nota.materia.nombre}: {round(nota.nota,2)}" for nota in notas)
                    procesar_salir()
                    return f"Las materias y notas del alumno con cédula {cedula} son:\n{materias_y_notas}"
                    cedula = ""
                else:
                    cedula = ""
                    return "El alumno no tiene materias registradas."
            except Persona.DoesNotExist:
                return "No se encontró un alumno con la cédula proporcionada."
        else:
            cedula = ""
            return "Número de cédula incorrecto. Proporciona un número de cédula de 10 dígitos."
    return "Por favor, proporciona la información solicitada."

def procesar_respuesta_mis_profesores_hijo(message):
    global profesores_hijob, cedula, usuario ,personalisada

    if usuario:
        parentesco = Parentesco.objects.filter(padre__cedula=usuario['cedula'])

    if personalisada:
        parentesco = Parentesco.objects.filter(padre__cedula=personalisada.cedula)

    if len(message) == 10 and message.isdigit():
        if not verificar_cedula(message):
            return "Número de cédula incorrecto. Proporciona un número de cédula valido."
        parentesco = Parentesco.objects.filter(padre__cedula=message)

    if parentesco:
        notas = Nota.objects.filter(alumno__in=parentesco.values_list('hijo', flat=True)).distinct()
        hijos_profesores = {}

        for nota in notas:
            hijo_nombre = nota.alumno.nombre
            profesor_nombre = nota.materia.curso.profesor.nombre

            # Agrega el nombre del hijo al diccionario si no existe
            if hijo_nombre not in hijos_profesores:
                hijos_profesores[hijo_nombre] = set()

            # Agrega el nombre del profesor al conjunto de profesores del hijo
            hijos_profesores[hijo_nombre].add(profesor_nombre)

        # Crear la cadena de texto con la información requerida
        resultado = []
        for hijo, profesores in hijos_profesores.items():
            profesores_str = ', '.join(profesores)
            resultado.append(f"Alumno:\n {hijo}\nProfesores:\n{profesores_str}")

        resultado_str = '\n'.join(resultado)
        profesores_hijob = False
        return resultado_str
    else:
        return "No tiene hijos registrados."


def procesar_respuesta_mis_cursosb(message):
    global mis_cursosb,cedula
    if message:
        if len(message) == 10 and message.isdigit():
            if not verificar_cedula(message):
                return "Número de cédula incorrecto. Proporciona un número de cédula valido."
            cedula = message
            try:
                persona = Persona.objects.get(cedula=cedula)
                if persona.tipo == "Profesor":
                    curso = Curso.objects.filter(profesor=persona)
                    if curso:
                        cursos = '\n'.join(f"- {curso.nombre}" for curso in curso)
                        procesar_salir()
                        return f"Sus cursos son:\n{cursos}"
                        cedula = ""
                    else:
                        cedula = ""
                        procesar_salir()
                        return "No tiene cursos registrad0s."
                else:
                    procesar_salir()
                    return "Usted no es docente"
            except Persona.DoesNotExist:
                return "No se encontró un docente con la cédula proporcionada."
        else:
            cedula = ""
            return "Número de cédula incorrecto. Proporciona un número de cédula de 10 dígitos."

    return "Por favor, proporciona la información solicitada."

def procesar_respuesta_registrarhijo(message):
    global registro_en_proceso, nombre, apellido, fecha_nacimiento, cedula, email
    doc = nlp(message)
    if not nombre:
        nombre = message
        return "Proporciona el apellido:"
    if not apellido:
       if message:
          apellido = message
          return "Proporciona la fecha de nacimiento (AAAA-MM-DD):"
       else:
          return "No pude reconocer el apellido. Por favor, proporciona el apellido."

    if not fecha_nacimiento:
        try:
            fecha = parse_date(message)
            fecha_nacimiento = fecha
            return "Proporciona el correo electrónico:"
        except ValueError:
            return "Formato de fecha incorrecto. Proporciona la fecha de nacimiento en el formato AAAA-MM-DD."

    if not email:
        if "@" in message and "." in message:
            email = message
            return "Proporciona el número de cédula:"
        else:
            return "Correo electrónico inválido. Proporciona un correo electrónico válido."

    if not cedula:
        if len(message) == 10 and message.isdigit():
            if not verificar_cedula(message):
                return "Número de cédula incorrecto. Proporciona un número de cédula valido."
            cedula = message
            return registrohijo()
        else:
            return "Número de cédula incorrecto. Proporciona un número de cédula de 10 dígitos."
    return "Por favor, proporciona la información solicitada."

def registrohijo():
    global registro_en_proceso, nombre, apellido, fecha_nacimiento, cedula, email,registrar_hijob, personalisada, usuario
    if personalisada:
        padre = Persona.objects.get(cedula=personalisada.cedula)
    if usuario:
        padre = Persona.objects.get(cedula=usuario['cedula'])
        return "Para comenzar el registro, por favor proporciona los nombres:"
    user = User.objects.create_user((nombre.split()[0] + apellido.split()[0]), email, 'password123', first_name=nombre,
                                    last_name=apellido)
    user.save()
    hijo = Persona(nombre=nombre,
                   apellidos=apellido,
                   cedula=cedula,
                   nacimiento=fecha_nacimiento,
                   email=email,
                   usuario=user,
                   tipo='Alumno')

    hijo.save()

    parentesco = Parentesco(padre=padre, hijo=hijo)
    parentesco.save()

    mensaje_confirmacion = (f"Los datos de tu hijo han sido registrados:\n"
                            f"Nombre: {nombre}\n"
                            f"Apellido: {apellido}\n"
                            f"Fecha de nacimiento: {fecha_nacimiento}\n"
                            f"Cédula: {cedula}")
    procesar_salir()
    return mensaje_confirmacion



def perfil(request):
    global usuario
    if usuario:
        return "perfil"
    return "No estas logeado?"

def ajustes(request):
    global usuario
    if usuario:
        return "ajustes"
    return "No estas logeado?"

def iniciar_misnotas():
    global mis_notas_alumno
    mis_notas_alumno = True
    return "Por favor, proporciona tu numero de cedula para conocer tus notas:"

def procesar_mis_notas_alumno(message):
    global mis_notas_alumno,cedula
    if len(message) == 10 and message.isdigit():
        if not verificar_cedula(message):
            return "Número de cédula incorrecto. Proporciona un número de cédula valido."
        cedula = message
        try:
            persona = Persona.objects.get(cedula=cedula)
            notas = Nota.objects.filter(alumno=persona).select_related('materia').distinct()
            if notas:
                materias_y_notas = '\n'.join(f"- {nota.materia.nombre}: {round(nota.nota, 2)}" for nota in notas)
                procesar_salir()
                return f"Las materias y notas de {persona.nombre} son:\n{materias_y_notas}"
                cedula = ""
            else:
                cedula = ""
                return "El alumno no tiene materias registradas."
        except Exception as e:
            return "No existe persona registrada con el numero de cedula ingresado"

def iniciar_cambio_contrasena():
    global cambio_contrasena_en_proceso
    cambio_contrasena_en_proceso = True
    return "Por favor, proporciona tu nombre de usuario para cambiar la contraseña:"

def procesar_respuesta_cambio_contrasena(message, request):
    global cambio_contrasena_en_proceso

    if 'username_cambio' not in request.session:
        request.session['username_cambio'] = message
        return "Por favor, proporciona tu contraseña actual:"

    if 'password_actual' not in request.session:
        request.session['password_actual'] = message
        return "Por favor, proporciona tu nueva contraseña:"

    if 'password_nueva' not in request.session:
        request.session['password_nueva'] = message
        username = request.session['username_cambio']
        password_actual = request.session['password_actual']
        password_nueva = request.session['password_nueva']

        try:
            user = auth.authenticate(username=username, password=password_actual)
            if user is not None:
                user.set_password(password_nueva)
                user.save()
                procesar_salir_cambio_contrasena(request)
                return "Contraseña cambiada exitosamente"
            else:
                procesar_salir_cambio_contrasena(request)
                return "Error: Contraseña actual incorrecta"
        except Exception as e:
            procesar_salir_cambio_contrasena(request)
            return f"Error en el cambio de contraseña: {str(e)}"

    return "Por favor, proporciona la información solicitada."


def iniciar_registro_materia_alumno():
    global registro_materia,usuario
    if usuario:
        if usuario['tipo'] == "Administrador":
            registro_materia = True
            return "Para comenzar el registro, por favor proporciona la cedula del alumno:"
        else:
            return "Solo los administradores pueden asignar materias a los alumnos"
    elif personalisada:
        if personalisada.tipo == "Administrador":
            registro_materia = True
            return "Para comenzar el registro, por favor proporciona la cedula del alumno:"
        else:
            return "Solo los administradores pueden asignar materias a los alumnos"
    else:
        return "Solo los administradores pueden asignar materias a los alumnos"

def procesar_registro_materias_alumno(message):
    try:
        global registro_materia, usuario , cedula ,curso,materia

        if len(message) == 10 and message.isdigit():
            if not verificar_cedula(message):
                return "Número de cédula incorrecto. Proporciona un número de cédula valido."
            cedula = message
            materias = Materia.objects.all()
            cursos_unicos = materias.values('curso','curso__nombre').distinct()
            cur = cursos_unicos

            cursos = '\n'.join(f"- {curso['curso__nombre']}" for curso in cursos_unicos)
            return f"Escoja el el curso:\n{cursos}"

        if not curso:
            curso = Curso.objects.filter(nombre=message).first()
            mat = Materia.objects.filter(curso=curso)
            materias = '\n'.join(f"-{mat.nombre}" for mat in mat)
            return f"Escoja la materia del curso:\n{materias}"
        if not materia:
            materia = Materia.objects.filter(nombre=message,curso=curso).first()

            persona = Persona.objects.get(cedula=cedula)
            item = Nota(
                alumno=persona,
                materia=materia,
                nota=0
            )
            item.save()
            registro_materia = False
            return "Se ha registrado la materia la alumno."
    except Exception as e:
       return f"Ingrese los datos solicitados. Error: {str(e)}"



def contacto_docente():
    global contacto_docenteb, personalisada, usuario
    contacto_docenteb = True
    if personalisada:
        return procesar_respuesta_contacto_docente(personalisada.cedula)
    if usuario:
        return procesar_respuesta_contacto_docente(usuario['cedula'])
    return "Para conocer el contacto de tus profesores, ingresa tu número de cédula:"


def procesar_respuesta_contacto_docente(message):
    global contacto_docenteb, cedula
    if message:
        if len(message) == 10 and message.isdigit():
            if not verificar_cedula(message):
                return "Número de cédula incorrecto. Proporciona un número de cédula valido."
            cedula = message
        if usuario:
            cedula = usuario['cedula']

        if personalisada:
            cedula = personalisada.cedula

        if cedula:
            alumno = Persona.objects.get(cedula=cedula, tipo='Alumno')
        else :
            return "Número de cédula incorrecto. Proporciona un número de cédula de 10 dígitos."
        try:
            notas = Nota.objects.filter(alumno=alumno).select_related('materia__curso__profesor').distinct()
            profesores_contacto = {nota.materia.curso.profesor: nota.materia.curso.profesor.email for nota in notas}
            if profesores_contacto:
                contacto_lista = '\n'.join(f"- {profesor.nombre} {profesor.apellidos}: {email}" for profesor, email in profesores_contacto.items())
                contacto_docenteb = False
                return f"Contactos de tus profesores:\n{contacto_lista}"
            else:
                contacto_docenteb = False
                return "No tienes profesores registrados."
        except Persona.DoesNotExist:
            return "No se encontró un alumno con la cédula proporcionada."
    return "Por favor, proporciona la información solicitada."


def mis_profesores():
    global mis_profesoresb, personalisada, usuario
    mis_profesoresb = True
    if personalisada:
        return procesar_respuesta_mis_profesores(personalisada.cedula)
    if usuario:
        return procesar_respuesta_mis_profesores(usuario['cedula'])
    return "Para conocer tus profesores, ingresa tu número de cédula:"

def procesar_respuesta_mis_profesores(message):
    global mis_profesoresb, cedula
    if message:
        if len(message) == 10 and message.isdigit():
            if not verificar_cedula(message):
                return "Número de cédula incorrecto. Proporciona un número de cédula valido."
            cedula = message
        if usuario:
            cedula = usuario['cedula']

        if personalisada:
            cedula = personalisada.cedula

        if cedula:
            alumno = Persona.objects.get(cedula=cedula, tipo='Alumno')
        else:
            return "Número de cédula incorrecto. Proporciona un número de cédula de 10 dígitos."
        try:
            notas = Nota.objects.filter(alumno=alumno).select_related('materia__curso__profesor').distinct()
            profesores = {nota.materia.curso.profesor for nota in notas}
            if profesores:
                profesores_lista = '\n'.join(f"- {profesor.nombre} {profesor.apellidos}" for profesor in profesores)
                mis_profesoresb = False
                return f"Tus profesores son:\n{profesores_lista}"
            else:
                mis_profesoresb = False
                return "No tienes profesores registrados."
        except Persona.DoesNotExist:
            return "No se encontró un alumno con la cédula proporcionada."
    return "Por favor, proporciona la información solicitada."

def mis_estudiantes():
    global mis_estudiantesb, personalisada, usuario
    mis_estudiantesb = True
    if personalisada:
        return procesar_respuesta_mis_estudiantes(personalisada.cedula)
    if usuario:
        return procesar_respuesta_mis_estudiantes(usuario['cedula'])
    return "Para conocer tus estudiantes, ingresa tu número de cédula:"

def procesar_respuesta_mis_estudiantes(message):
    global mis_estudiantesb, cedula
    if message:
        if len(message) == 10 and message.isdigit():
            if not verificar_cedula(message):
                return "Número de cédula incorrecto. Proporciona un número de cédula valido."
            cedula = message
        if usuario:
            cedula = usuario['cedula']

        if personalisada:
            cedula = personalisada.cedula

        if cedula:
            profesor = Persona.objects.get(cedula=cedula, tipo='Profesor')
        else:
            return "Número de cédula incorrecto. Proporciona un número de cédula de 10 dígitos."
        try:
            cursos = Curso.objects.filter(profesor=profesor)
            estudiantes = Persona.objects.filter(nota__materia__curso__in=cursos).distinct()
            if estudiantes:
                estudiantes_lista = '\n'.join(f"- {estudiante.nombre} {estudiante.apellidos}" for estudiante in estudiantes)
                mis_estudiantesb = False
                return f"Tus estudiantes son:\n{estudiantes_lista}"
            else:
                mis_estudiantesb = False
                return "No tienes estudiantes registrados."
        except Persona.DoesNotExist:
            return "No se encontró un profesor con la cédula proporcionada."
    return "Por favor, proporciona la información solicitada."


def contacto_docente_materia():
    global contacto_docente_materia_b, personalisada, usuario
    contacto_docente_materia_b = True
    if personalisada:
        return procesar_respuesta_contacto_docente_materia(personalisada.cedula)
    if usuario:
        return procesar_respuesta_contacto_docente_materia(usuario['cedula'])
    return "Para conocer el contacto de docentes por materia, ingresa tu número de cédula:"

def procesar_respuesta_contacto_docente_materia(message):
    global contacto_docente_materia_b, cedula, usuario ,personalisada

    if len(message) == 10 and message.isdigit():
        if not verificar_cedula(message):
            return "Número de cédula incorrecto. Proporciona un número de cédula valido."
        cedula = message

    if usuario:
        cedula = usuario['cedula']

    if personalisada:
        cedula = personalisada.cedula

    if cedula:
        parentesco = Parentesco.objects.filter(padre__cedula=cedula)
    else:
        return "Número de cédula incorrecto. Proporciona un número de cédula de 10 dígitos."

    if parentesco:
        notas = Nota.objects.filter(alumno__in=parentesco.values_list('hijo', flat=True)).distinct()
        hijos_profesores = {}

        for nota in notas:
            hijo_nombre = nota.alumno.nombre
            materia_nombre = nota.materia.nombre
            profesor_nombre = nota.materia.curso.profesor.nombre
            profesor_email = nota.materia.curso.profesor.email

            # Agrega el nombre del hijo al diccionario si no existe
            if hijo_nombre not in hijos_profesores:
                hijos_profesores[hijo_nombre] = []

            # Agrega la información del profesor al conjunto de profesores del hijo
            hijos_profesores[hijo_nombre].append({
                'materia': materia_nombre,
                'profesor': profesor_nombre,
                'contacto': profesor_email
            })

        # Crear la cadena de texto con la información requerida
        resultado = []
        for hijo, profesores in hijos_profesores.items():
            profesores_info = '\n'.join(
                f"Materia: {prof['materia']}\nProfesor: {prof['profesor']}\nContacto:\n{prof['contacto']}" for prof in
                profesores)
            resultado.append(f"Alumno:\n{hijo}\n{profesores_info}")

        resultado_str = '\n'.join(resultado)
        contacto_docente_materia_b = False
        return resultado_str
    else:
        contacto_docente_materia_b = False
        return "No tiene hijos registrados."

def get_session_tp(request):
    if request.session.get('usuario'):
        tp = request.session['usuario'].get('tipo')
        return JsonResponse({'tp': tp})

    tp = request.session.get('tp', 'Persona')  # Retorna 'Persona' si 'tp' no está en la sesión
    return JsonResponse({'tp': tp})

def procesar_salir():
    global contacto_docente_materia_b,mis_profesoresb,contacto_docenteb,profesores_hijob,personalisada,\
        registro_en_proceso,login_en_proceso,mis_materiasb,mis_cursosb,registrar_hijob,notas_hijob,personalisada,\
        cambio_contrasena_en_proceso, usuario,nombre,apellido,fecha_nacimiento,cedula,email,curso,materia
    registro_en_proceso = False
    login_en_proceso = False
    mis_materiasb = False
    mis_cursosb = False
    registrar_hijob = False
    notas_hijob = False
    profesores_hijob = False
    cambio_contrasena_en_proceso = False
    contacto_docenteb = False
    mis_profesoresb = False
    contacto_docente_materia_b = False
    usuario = None
    nombre = ""
    apellido = ""
    fecha_nacimiento = ""
    cedula = ""
    email = ""
    personalisada = ""
    curso = ""
    materia = ""

    return "Hola👋 Como puedo ayudarte %s." % personalisada


def procesarpersonalizada(request):
    global contacto_docente_materia_b,mis_profesoresb,contacto_docenteb,profesores_hijob,registro_en_proceso,login_en_proceso,mis_materiasb,mis_cursosb,registrar_hijob,notas_hijob,personalisada,cambio_contrasena_en_proceso
    registro_en_proceso = False
    login_en_proceso = False
    mis_materiasb = False
    mis_cursosb = False
    registrar_hijob = False
    notas_hijob = False
    profesores_hijob = False
    contacto_docenteb = False
    mis_profesoresb = False
    personalisada = ""
    cambio_contrasena_en_proceso = False
    contacto_docente_materia_b = False
    if request.session.get('tp'):
        del request.session['tp']
    return "Hola👋 Como puedo ayudarte?"

def procesar_salir_cambio_contrasena(request):
    del request.session['username_cambio']
    del request.session['password_actual']
    del request.session['password_nueva']
    procesar_salir()
