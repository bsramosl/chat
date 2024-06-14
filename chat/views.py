import datetime

from django.contrib.auth.models import User
from django.shortcuts import *
from django.http import JsonResponse, HttpResponse
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import spacy

from chat.models import Persona

# Cargar el modelo de spaCy para español
nlp = spacy.load('es_core_news_md')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
nlp = spacy.load('es_core_news_md')

registro_en_proceso = False
nombre = ""
apellido = ""
fecha_nacimiento = ""
cedula = ""
email = ""



def Index(request):
    return render(request,'index.html')


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        body = data.get('message')
        try:
            response_text = generate_response(body)
            return JsonResponse({'success': True, 'message': response_text})
        except Exception as e:
            return JsonResponse({'error': f"Failed to process message: {e}"}, status=500)
    else:
        return JsonResponse({'error': "This endpoint only accepts POST requests."}, status=405)




def generate_response(message):
    global registro_en_proceso

    message = message.lower()
    doc = nlp(message)

    # Si no hay un proceso de registro en curso, procesar como de costumbre
    if not registro_en_proceso:
    
        responses = {
            "hola": "¡Hola! ¿Cómo puedo ayudarte hoy?",
            "adiós": "¡Adiós! Que tengas un buen día.",
            "cómo estás": "Estoy bien, gracias por preguntar. ¿Y tú?",
            "qué puedes hacer": "Puedo responder preguntas básicas. ¿Qué te gustaría saber?",
            "quién eres": "Soy un chatbot creado para ayudarte. ¿En qué puedo asistirte?",
            "gracias": "De nada. ¿Hay algo más en lo que pueda ayudarte?",
            "cómo me puedo registrar": "Para registrarte, puedes iniciar el proceso escribiendo 'registro'.",
            "cuáles son los requisitos": "Los requisitos para registrarse incluyen nombre completo, fecha de nacimiento, correo electrónico y número de cédula.",
            "cómo registro a mi hijo": "Para registrar a tu hijo, por favor proporciona los detalles de su nombre, fecha de nacimiento y número de identificación.",
            "qué cursos hay": "Actualmente ofrecemos una variedad de cursos. Por favor visita nuestra página web para más detalles.",
            "registro": iniciar_registro,
            "cuánto cuesta el registro": "El costo del registro varía dependiendo del curso. Por favor, visita nuestra página de tarifas para más detalles.",
            "dónde están ubicados": "Nuestra institución está ubicada en la calle Principal #123, Ciudad, País.",
            "cuál es su horario de atención": "Nuestro horario de atención es de lunes a viernes, de 9:00 AM a 6:00 PM.",
            "ofrecen cursos en línea": "Sí, ofrecemos una variedad de cursos en línea. Visita nuestra página web para más información.",
            "cuánto duran los cursos": "La duración de los cursos varía. Algunos son de unas pocas semanas, mientras que otros pueden durar varios meses.",
            "qué documentos necesito para el registro": "Necesitas tu identificación oficial, comprobante de domicilio y los documentos específicos del curso que elijas.",
            "cómo puedo contactar con soporte": "Puedes contactar con soporte enviando un correo a soporte@nuestraescuela.com o llamando al (123) 456-7890.",
            "hay descuentos disponibles": "Sí, ofrecemos descuentos para estudiantes, miembros de la misma familia y pagos anticipados.",
            "cómo puedo pagar": "Aceptamos pagos con tarjeta de crédito, débito y transferencias bancarias.",
            "puedo visitar las instalaciones": "Sí, puedes agendar una visita a nuestras instalaciones llamando al (123) 456-7890.",
            "hay plazas disponibles": "La disponibilidad de plazas varía según el curso. Por favor, consulta nuestra página web para información actualizada.",
            "cómo cancelo mi inscripción": "Para cancelar tu inscripción, por favor contacta con nuestro soporte.",
            "qué pasa si pierdo una clase": "Si pierdes una clase, puedes ponerte al día accediendo a los materiales en línea o contactando a tu instructor.",
            "hay actividades extracurriculares": "Sí, ofrecemos una variedad de actividades extracurriculares como deportes, artes y clubes académicos.",
            "puedo cambiar de curso": "Sí, puedes solicitar un cambio de curso contactando con soporte.",
            "cómo se evalúa a los estudiantes": "La evaluación de los estudiantes se realiza a través de exámenes, proyectos y participación en clase.",
            "hay becas disponibles": "Sí, ofrecemos becas para estudiantes destacados y aquellos con necesidades financieras.",
            "cuándo comienzan los cursos": "Los cursos comienzan en diferentes fechas a lo largo del año. Consulta nuestra página web para el calendario de inicio.",
            "puedo inscribirme a más de un curso": "Sí, puedes inscribirte a varios cursos, siempre y cuando no haya conflictos de horario.",
            "qué nivel de español necesito": "Nuestros cursos están diseñados para hablantes nativos y avanzados de español. Consulta los requisitos específicos del curso.",
            "cómo accedo a los materiales del curso": "Los materiales del curso están disponibles en nuestra plataforma en línea, a la cual tendrás acceso una vez inscrito.",
            "tienen estacionamiento": "Sí, nuestras instalaciones cuentan con estacionamiento gratuito para estudiantes.",
            "hay transporte escolar": "Ofrecemos transporte escolar en áreas seleccionadas. Consulta con soporte para más información.",
            "puedo hablar con un instructor": "Sí, puedes agendar una cita para hablar con un instructor contactando con soporte.",
            "qué pasa si tengo una emergencia y no puedo asistir": "En caso de emergencia, notifica a soporte y haremos los arreglos necesarios para que no pierdas contenido importante.",
            "cómo se manejan las ausencias": "Las ausencias deben justificarse a través de soporte. Se permiten un número limitado de ausencias justificadas por curso.",
            "hay tutorías disponibles": "Sí, ofrecemos tutorías personalizadas. Consulta con soporte para más detalles.",
            "cómo accedo a mi cuenta en línea": "Puedes acceder a tu cuenta en línea desde nuestra página web usando tu correo electrónico y contraseña."
        }

        # Procesar la similitud con las respuestas predefinidas
        for question, response in responses.items():
            question_doc = nlp(question)
            similarity = doc.similarity(question_doc)
            if similarity > 0.75:  # Umbral de similitud
                if callable(response):
                    # Si la respuesta es una función, llamarla y devolver el resultado
                    return response()
                else:
                    return response

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
        for ent in doc.ents:
            if ent.label_ == 'PER':
                nombre = ent.text
                return "Proporciona tu apellido:"
        return "No pude reconocer tu nombre. Por favor, proporciona tu nombre."

    if not apellido:
        for ent in doc.ents:
            if ent.label_ == 'PER':
                apellido = ent.text
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
            cedula = message
            return registro()
        else:
            return "Número de cédula incorrecto. Proporciona un número de cédula de 10 dígitos."
    return "Por favor, proporciona la información solicitada."


def registro():
    global registro_en_proceso, nombre, apellido, fecha_nacimiento, cedula ,email
    registro_en_proceso = False
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
    return mensaje_confirmacion