from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import pytz

app = Flask(__name__)

SHOP_NAME = "RJ TRENDZ"
ADDRESS = "Ravikamtham Village, Ravikamtham Mandalam"
TIMINGS = "Morning 10:00 AM nundi Night 11:00 PM varuku"
PRICES = "Shirts Rs.499 nundi, Pants Rs.799 nundi start"

def get_wish():
    ist = pytz.timezone('Asia/Kolkata')
    hour = datetime.now(ist).hour
    if 5 <= hour < 12: return "Good Morning"
    elif 12 <= hour < 17: return "Good Afternoon"
    elif 17 <= hour < 21: return "Good Evening"
    else: return "Good Night"

@app.route("/")
def home():
    return f"{SHOP_NAME} Bot Live Undi!"

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming = request.values.get('Body', '').lower().strip()
    resp = MessagingResponse()
    msg = resp.message()
    wish = get_wish()

    # HI
    if any(x in incoming for x in ["hi", "hello", "hey", "namaste", "hlo"]):
        msg.body(f"{wish} 🙏\n\nWelcome to {SHOP_NAME} 👕\n\nMeeku emi kavali cheppandi:\n• Shirts / T-Shirts\n• Pants / Jeans\n• Price / Rate\n• Address / Location\n• Timings\n\nEdi adigina chepta bhayya!")

    # SHIRTS
    elif any(x in incoming for x in ["shirt", "tshirt", "t-shirt"]):
        msg.body(f"Shirts lo manadaggara:\n👕 Plain Shirts - Rs.499+\n👕 Colour Shirts - Rs.599+\n👕 Checks & Printed kuda undi\n\nSize? M, L, XL anni unnai bhayya!")

    # PANTS
    elif any(x in incoming for x in ["pant", "jeans", "trouser"]):
        msg.body(f"Pants lo manadaggara:\n👖 Jeans - Rs.799+\n👖 Formal Pants with Belt - Rs.899+\n👖 Black, Blue, Grey colours unnayi!")

    # PRICE
    elif any(x in incoming for x in ["price", "rate", "cost", "entha", "dhara"]):
        msg.body(f"Price Details 💰\n{PRICES}\n\nOffer kuda undi bhayya, shop ki vaste thaggistham!")

    # ADDRESS / LOCATION
    elif any(x in incoming for x in ["address", "location", "ekkada", "where"]):
        msg.body(f"📍 {SHOP_NAME}\n{ADDRESS}\n\nRavikamtham main road lone bhayya!")

    # TIMINGS
    elif any(x in incoming for x in ["timing", "time", "open", "close"]):
        msg.body(f"⏰ Timings: {TIMINGS}\nPrathi roju open bhayya!")

    # SMART REPLY FOR ANY OTHER CLOTH QUESTION - No need to add code again!
    else:
        msg.body(f"{wish} bhayya! 🙏\n\nMeeru adigindi '{incoming}' ki sambandhinchi...\n\nManadaggara {SHOP_NAME} lo Shirts, Pants, Jeans anni trendy collection unnayi. {PRICES}. Meeku size, colour chepte pic kuda pedtham!\n\nShop ki okasari randi, nachina item teesukondi!")

    return str(resp)
