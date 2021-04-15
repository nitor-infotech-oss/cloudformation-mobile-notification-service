import os
from twilio.rest import Client
import config as c
import json

def send_sms(client, to, msg):
    client.messages.create(
                from_=c.SMS_NUMBER,
                body=msg,
                to=to
            )

def send_whatsapp_message(client, to, msg):
    client.messages.create(
                from_=c.WHATSAPP_NO,
                body=msg,
                to='whatsapp:+918600299002'
            )

def handler(event, context):
    print("EVENT: ", event)
    print("CONTEXT: ", context)
    if not ("to" in event.keys() and "msg" in event.keys()) or (event["msg_type"].lower() not in ["whatsapp", "sms"]):
        message = { "error": "Invalid Parameters" }
    else:
        to       = event["to"]
        msg      = event["msg"]
        msg_type = event["msg_type"]
        try:
            client = Client(c.TWILIO_SID, c.TWILIO_TOKEN)
            if (msg_type.lower() == "whatsapp"):
                send_whatsapp_message(client, to, msg)
            elif (msg_type.lower() == "sms"):
                send_sms(client, to, msg)
            message = { "success": "Message sent successfully" }
        except:
            message = {
                "error": "Failed to send message."
            }
    return json.dumps(message)
