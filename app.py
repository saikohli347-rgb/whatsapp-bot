from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is Live!"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    msg_body = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    reply = resp.message()
    if 'hi' in msg_body:
        reply.body("Hi! I am your WhatsApp bot on Render 🤖")
    else:
        reply.body(f"You sent: {msg_body}")
    return str(resp)
