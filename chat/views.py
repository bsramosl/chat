from django.shortcuts import *
from django.http import JsonResponse, HttpResponse
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import spacy

# Cargar el modelo de spaCy para español
nlp = spacy.load('es_core_news_md')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
nlp = spacy.load('es_core_news_md')

registro_en_proceso = False

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
            "registro": iniciar_registro
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
    return "Para comenzar el registro, por favor proporciona tu nombre completo:"


def procesar_respuesta_registro(message):
    global registro_en_proceso,nombre_completo, fecha_nacimiento, cedula

    # Verificar si el mensaje contiene información sobre el nombre
    doc = nlp(message)
    for ent in doc.ents:
        if ent.label_ == 'PER':
            nombre_completo = ent.text
            # Si se encuentra el nombre, solicitar fecha de nacimiento
            return "Proporciona tu fecha de nacimiento (AAAA-MM-DD):"
    fecha = parse_date(message)
    if fecha:
        fecha_nacimiento = message
        return "Proporciona tu número de cedula:"

    if len(message) == 10 and message.isdigit():
        if message:
            cedula = message
            regitro()
    registro_en_proceso = True
    return "Por favor, proporciona la información solicitada."


def regitro():
    return "Tu esta registrado verifica tu correo"