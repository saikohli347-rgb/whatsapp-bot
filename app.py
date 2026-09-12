import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq

app = Flask(__name__)

# Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return "Mama Bot Live with Groq Free! 🔥"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "")
    print(f"User msg: {incoming_msg}")

    try:
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a friendly assistant. Always reply in Telugu slang using 'mama'. Keep it fun and helpful."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply_text = chat.choices[0].message.content
        print(f"Bot reply: {reply_text}")
    except Exception as e:
        print(f"Error: {e}")
        reply_text = "Mama konchem technical issue, malli try chey mama!"

    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)

if __name__ == "__main__":
    app.run()
