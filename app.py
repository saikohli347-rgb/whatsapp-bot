import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq

app = Flask(__name__)

@app.route("/")
def home():
    return "Mama Bot Live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "")
    print(f"Got msg: {incoming_msg}")
    api_key = os.environ.get("GROQ_API_KEY")
    print(f"Key exists: {bool(api_key)}")

    try:
        client = Groq(api_key=api_key)
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are friendly Telugu assistant, reply in Telugu slang with 'mama'."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply_text = chat.choices[0].message.content
    except Exception as e:
        print(f"Groq Error Full: {e}")
        reply_text = f"Mama error: {str(e)[:200]}"

    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)

if __name__ == "__main__":
    app.run()
