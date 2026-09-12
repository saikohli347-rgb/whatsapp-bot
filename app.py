from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import pytz
app = Flask(__name__)
SHOP_NAME = "SAI TRENDZ"
ADDRESS = "Ravikamtham Village, Ravikamtham Mandalam"
TIMINGS = "Morning 10:00 AM nundi Night 11:00 PM varuku"
def get_wish():
    ist = pytz.timezone('Asia/Kolkata')
    hour = datetime.now(ist).hour
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 17:
        return "Good Afternoon"
    elif 17 <= hour < 21:
        return "Good Evening"
    else:
        return "Good Night"
@app.route("/")
def home():
    return f"{SHOP_NAME} Bot Live Undi!"
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get('Body', '').lower().strip()
    resp = MessagingResponse()
    msg = resp.message()
    wish = get_wish()
    if any(x in incoming_msg for x in ["hi", "hello", "hey", "namaste"]):
        msg.body(f"{wish} 🙏\n\nWelcome to {SHOP_NAME} 👕👖\n\nMeeku emi kavali?\n1. Shirts\n2. Pants\n3. Shop Address\n4. Timings\n\nCheppandi bhayya!")
    elif "shirt" in incoming_msg or incoming_msg == "1":
        msg.body("Shirts lo Plain ha Colourful ha kavali? Plain Rs.499 nundi, Colourful Rs.599 nundi start bhayya!")
    elif "pant" in incoming_msg or "jeans" in incoming_msg or incoming_msg == "2":
        msg.body("Pants lo Jeans undi, Formal Pants with Belt tho kuda undi. Meeku edi kavali?")
    elif "address" in incoming_msg or "ekkada" in incoming_msg or incoming_msg == "3":
        msg.body(f"Address 📍\n{SHOP_NAME}\n{ADDRESS}")
    elif "timing" in incoming_msg or "time" in incoming_msg or incoming_msg == "4":
        msg.body(f"Timings ⏰\n{TIMINGS}\nPrathi roju open")
    else:
        msg.body(f"{wish} bhayya! Nenu {SHOP_NAME} bot ni. Shirts, Pants, Address, Timings edaina adagandi!")
    return str(resp)
