from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = "Nuvvu RJ TRENDZ shop assistant vi. Telugu lo friendly ga matladu mama, andi ani. Ravikamtham lo sarees, kurthis unnai ani cheppu."

@app.route('/')
def home():
    return "RJ TRENDZ BOT RUNNING MAMA!"

@app.route('/webhook', methods=['POST'])
def webhook():
    user_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ]
        )
        reply = completion.choices[0].message.content
        resp.message(reply)
    except Exception as e:
        print(f"Error: {e}")
        resp.message("Mama konchem technical issue, malli try cheyyi andi!")
    return str(resp)

if __name__ == "__main__":
    app.run()
