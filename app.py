import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return "Mama Bot Live with Groq Free! 🔥"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "")
    print(f"User: {incoming_msg}")
    try:
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a friendly assistant. Reply in Telugu slang like 'mama' style."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply_text = chat.choices[0].message.content
    except Exception as e:
        print(f"Groq Error: {e}")
        reply_text = f"Mama error: {e}"

    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)
