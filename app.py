from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

# === IDKKADA NUVVU MARCHALI ===
WHATSAPP_TOKEN = "NUVVU_COPY_CHESINA_TEMP_TOKEN_IKKADA_PETTU"
PHONE_NUMBER_ID = "NEE_PHONE_NUMBER_ID_IKKADA_PETTU"
OPENAI_API_KEY = "NEE_OPENAI_API_KEY_IKKADA_PETTU"
VERIFY_TOKEN = "rjtrendz123" # Idhi alaane unchanu

client = OpenAI(api_key=OPENAI_API_KEY)

# Shop gurinchi AI ki cheppu
SYSTEM_PROMPT = """
Nuvvu RJ TRENDZ, Ravikamtham lo unna best dress shop vi.
Owner Ravi Anna.
Nee style: Friendly Telugu lo matladu, 'mama', 'andi' ani piluvu.
Collections: Sarees, Kurthis, Kids wear, Mens wear. Low price lo best quality.
Address: Ravikamtham Main Road.
Customer adigina daniki helpful ga reply ivvu. Ammakaniki try cheyyi.
Short ga, 2-3 lines lo reply ivvu. Emojis vaddu ekkuva.
"""

@app.route('/')
def home():
    return "RJ TRENDZ AI BOT RUNNING MAMA!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Verification failed"

    if request.method == 'POST':
        data = request.json
        try:
            entry = data['entry'][0]['changes'][0]['value']
            if 'messages' in entry:
                msg = entry['messages'][0]
                from_number = msg['from']
                user_text = msg['text']['body']

                # OpenAI ki pampadam
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_text}
                    ]
                )
                ai_reply = response.choices[0].message.content

                # WhatsApp ki reply pampadam
                url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
                headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
                payload = {
                    "messaging_product": "whatsapp",
                    "to": from_number,
                    "text": {"body": ai_reply}
                }
                requests.post(url, headers=headers, json=payload)

        except Exception as e:
            print(f"Error: {e}")
        return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
