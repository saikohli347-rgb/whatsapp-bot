import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq

app = Flask(__name__)

@app.route("/")
def home():
    return "Live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    msg = request.values.get("Body", "")
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        chat = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are friendly Telugu assistant reply with mama slang"},
                {"role": "user", "content": msg}
            ]
        )
        reply = chat.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        reply = f"Error: {e}"
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run()
