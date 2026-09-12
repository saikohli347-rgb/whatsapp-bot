from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import pytz

app = Flask(__name__)

# Shop Details
SHOP_NAME = "RJ TRENDZ"
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

    # 1. Starting / Greeting
    if any(x in incoming_msg for x in ["hi", "hello", "hey", "namaste", "hii"]):
        reply = f"""{wish} 🙏

Welcome to {SHOP_NAME} 👕👖

Meeku emi kavali cheppandi?

1. Shirts 👔
2. Pants 👖
3. Shop Address 📍
4. Timings ⏰

Number type cheyandi leda peru rayandi (Ex: Shirts)"""
        msg.body(reply)

    # 2. Shirts
    elif "shirt" in incoming_msg or incoming_msg == "1":
        reply = f"""{SHOP_NAME} lo Shirts Unnayi 👔

Meeku elanti Shirts kavali?

A) Plain Shirts
B) Colourful / Printed Shirts

Meeku nachina type cheppandi, nenu photos & price pampista 😊

Meeru 'Pants' ani kuda adagavachu."""
        msg.body(reply)

    elif "plain" in incoming_msg and "shirt" in incoming_msg or incoming_msg == "a":
        msg.body("Plain Shirts lo mana deggara chala colours unnayi - White, Black, Blue, Cream. Price Rs.499 nundi start. Mee size enti? M, L, XL?")

    elif "colour" in incoming_msg or "colorful" in incoming_msg or "printed" in incoming_msg or incoming_msg == "b":
        msg.body("Colourful Shirts super collection undi bhayya! Checks, Prints, Party wear. Price Rs.599 nundi start. Meeru shop ki vasthe full collection chupista. Address kavala?")

    # 3. Pants
    elif "pant" in incoming_msg or "jeans" in incoming_msg or incoming_msg == "2":
        reply = """Pants lo rendu rakalu unnayi bhayya 👖

1. Jeans Pants
2. Formal Pants with Belt / Coat tho kuda veyavachu

Meeku edi kavali cheppandi?

Jeans ante Slim Fit, Regular Fit unnayi. Formal ante Plane colours."""
        msg.body(reply)

    # 4. Address
    elif "address" in incoming_msg or "location" in incoming_msg or "ekkada" in incoming_msg or "place" in incoming_msg or incoming_msg == "3":
        msg.body(f"""Mana Shop Address 📍

{SHOP_NAME}
{ADDRESS}

Google Maps location kavala ante 'Location' ani pampandi.""")

    # 5. Timings
    elif "timing" in incoming_msg or "time" in incoming_msg or "eppudu" in incoming_msg or incoming_msg == "4":
        msg.body(f"Shop Timings ⏰\n\n{TIMINGS} \nPrathi roju open untundi bhayya!")

    elif "cost" in incoming_msg or "price" in incoming_msg or "rate" in incoming_msg:
        msg.body("Prices chaala takkuva bhayya! Shirts Rs.499 nundi, Pants Rs.699 nundi start. Offer kuda nadustundi. Shop ki randi, manchiga chusi teesukovachu.")

    else:
        # Default
        msg.body(f"{wish} bhayya! Nenu {SHOP_NAME} bot ni. \n\nMeeku emi kavali? \nShirts, Pants, Address, Timings - edaina adagandi, Telugu lo ne chepta 😊")

    return str(resp)

if __name__ == "__main__":
    app.run()
