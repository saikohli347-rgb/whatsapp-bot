from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)
openai.api_key = "NEE_OPENAI_KEY_IKKADA_PETTU"

SYSTEM_PROMPT = "Nuvvu RJ TRENDZ shop assistant vi. Telugu lo friendly ga matladu mama, andi ani. Ravikamtham lo sarees, kurthis ammuthav. Short ga reply ivvu."

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
        ai_reply = completion.choices[0].message.content
        resp.message(ai_reply)
    except Exception as e:
        print(e)
        resp.message("Mama konchem busy ga unna, malla try cheyyi andi!")
    return str(resp)
