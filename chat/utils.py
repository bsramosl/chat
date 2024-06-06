from twilio.rest import Client
from django.conf import settings

def send_whatsapp_message(to, body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    from_whatsapp_number = settings.TWILIO_WHATSAPP_NUMBER
    to_whatsapp_number = f'whatsapp:{to}'

    client.messages.create(body=body,
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)