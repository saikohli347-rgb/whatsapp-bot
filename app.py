import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq

app = Flask(__name__)

# RJ TRENDZS - MEE SHOP DATA MAMA
SHOP_DATA = {
    "offers": "🔥 RJ TRENDZS MEGA OFFER MAMA! 🔥\n\n👕 Shirts - 2 @ 999/-\n👖 Jeans - 50% OFF\n👔 Formal Combo - 1499/-\n🎁 2000 pai konithe FREE Cap!\n\nLocation: Mancherial Road, Asifabad",
    "shirts": "👕 SHIRTS COLLECTION MAMA:\n\n1. Checks - 599/-\n2. Plain Formal - 699/-\n3. Printed Party Wear - 799/-\n4. Linen Cotton - 849/-\n\nSize: M, L, XL, XXL anni unnai mama!",
    "pants": "👖 PANTS & JEANS MAMA:\n\n1. Slim Fit Jeans - 899/-\n2. Formal Pant - 799/-\n3. Cargo 6 Pocket - 999/-\n4. Joggers - 699/-\n\nOffer lo 2 teeskunte 1599/- ke mama!",
    "timings": "🕘 Shop Timings: 9AM - 9:30PM\n📍 RJ Trendzs, Bus Stand Deggara"
}

@app.route("/")
def home():
    return "RJ TRENDZS Bot Live Mama!"

@app.route("/webhook", methods=["POST"])
def webhook():
    msg = request.values.get("Body", "").lower().strip()
    print(f"Customer: {msg}")

    # 1. SHOP KEYWORDS MAMA - Direct Reply
    reply = None
    if "offer" in msg or "discount" in msg or "rate" in msg:
        reply = SHOP_DATA["offers"]
    elif "shirt" in msg:
        reply = SHOP_DATA["shirts"] + "\n\n" + SHOP_DATA["offers"]
    elif "pant" in msg or "jean" in msg:
        reply = SHOP_DATA["pants"] + "\n\n" + SHOP_DATA["offers"]
    elif "time" in msg or "where" in msg or "location" in msg:
        reply = SHOP_DATA["timings"]
    elif "hi" in msg or "hey" in msg or "hlo" in msg:
        reply = "Hii Mama! 🙏 RJ TRENDZS ki Welcome!\n\n👕 Shirts kavala? \n👖 Pants kavala?\n🔥 Offers kavala?\n\nEm kavalo cheppu mama!"

    # 2. Verevanni AI tho reply mama
    if not reply:
        try:
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            chat = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": "You are RJ TRENDZS Asifabad clothing shop salesman. Reply in Telugu slang with 'mama', short. You sell shirts, pants, jeans. Always try to bring customer to shop. Owner is helpful."},
                    {"role": "user", "content": msg}
                ]
            )
            reply = chat.choices[0].message.content
        except Exception as e:
            reply = SHOP_DATA["offers"] + "\n\nMama shop ki randi direct ga chupista!"

    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run()
