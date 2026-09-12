import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

app = Flask(__name__)

# Groq client - free & fast
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

@app.route("/")
def home():
    return "Mama Bot Live with Groq Free! 🔥"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "")
    print(f"User: {incoming_msg}")

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a friendly assistant. Reply in Telugu slang like 'mama' style, helpful and fun."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply_text = response.choices[0].message.content
        print(f"Bot: {reply_text}")

    except Exception as e:
        print(f"Groq Error: {e}")
        reply_text = "Mama Groq key check chey andi! Key thappu undi."

    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)

if __name__ == "__main__":
    app.run()
