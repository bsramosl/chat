from django.shortcuts import *
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import spacy

# Cargar el modelo de spaCy para español
nlp = spacy.load('es_core_news_md')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
nlp = spacy.load('es_core_news_md')
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
    message = message.lower()
    doc = nlp(message)

    # Respuestas predeterminadas
    responses = {
        "hola": "¡Hola! ¿Cómo puedo ayudarte hoy?",
        "adiós": "¡Adiós! Que tengas un buen día.",
        "cómo estás": "Estoy bien, gracias por preguntar. ¿Y tú?",
        "qué puedes hacer": "Puedo responder preguntas básicas. ¿Qué te gustaría saber?",
        "quién eres": "Soy un chatbot creado para ayudarte. ¿En qué puedo asistirte?",
        "gracias": "De nada. ¿Hay algo más en lo que pueda ayudarte?",
    }

    # Entidades reconocidas por spaCy
    entities = {ent.label_: ent.text for ent in doc.ents}

    # Ejemplo de lógica adicional utilizando las entidades reconocidas
    if 'PERSON' in entities:
        return f"¡Hola {entities['PERSON']}! ¿En qué puedo ayudarte?"

    # Procesar la similitud con las respuestas predefinidas
    for question, response in responses.items():
        question_doc = nlp(question)
        similarity = doc.similarity(question_doc)
        if similarity > 0.75:  # Umbral de similitud
            return response

    return "Lo siento, no entiendo tu pregunta."