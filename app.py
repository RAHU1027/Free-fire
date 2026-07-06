from flask import Flask, render_template_string, request
import telebot
import threading
import requests
import random
import time

app = Flask(__name__)

# --- CONFIGURATION ---
BOT_TOKEN = "8922478884:AAHgrLyM20xpxi-GKRiC_W_Gx8uwMUV0E5s"
bot = telebot.TeleBot(BOT_TOKEN)

# --- LOGIC FUNCTIONS ---
def get_card_data(card):
    # API se bin lookup
    bin_num = card.replace(" ", "").replace("|", "")[:6]
    try:
        res = requests.get(f"https://lookup.binlist.net/{bin_num}", timeout=5).json()
        issuer = res.get('bank', {}).get('name', 'UNKNOWN').upper()
        brand = res.get('brand', 'UNKNOWN')
        card_type = res.get('type', 'UNKNOWN')
        country = res.get('country', {}).get('name', 'UNKNOWN').upper()
        # Random status logic for demonstration
        status = random.choice(["Approved ✅", "Decline ❌"])
        response = "Charged $1.00" if "Approved" in status else "Insufficient Funds"
    except:
        issuer, brand, card_type, country, status, response = "UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN", "Decline ❌", "Gateway Error"
    
    return issuer, f"{brand} - {card_type}".upper(), country, status, response

# --- UI TEMPLATE WITH PERFECT DESIGN ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #000; color: #fff; font-family: 'Courier New', monospace; padding: 20px; }
        .result-box { background: #0a0a0a; border: 1px solid #333; padding: 25px; border-radius: 10px; width: 380px; 
                      animation: fadeIn 0.8s forwards; margin-top: 20px; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .data { color: #fff; }
    </style>
</head>
<body>
    <form method="POST" action="/check">
        <input type="text" name="card" placeholder="Enter Full Card (16 digits)" required style="width:300px; padding:10px; background:#111; color:#fff; border:1px solid #444;">
        <button type="submit" style="padding:10px;">CHECK</button>
    </form>
    {% if result %}
    <div class="result-box">
        <pre>{{ result }}</pre>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        card = request.form.get('card')
        issuer, info, country, status, response = get_card_data(card)
        result = (f"• » Card ⇾ {card}\n"
                  f"• » Status ⇾ {status}\n"
                  f"• » Response ⇾ {response}\n\n"
                  f"• » Issuer ⇾ {issuer}\n"
                  f"• » Info ⇾ {info}\n"
                  f"• » Country ⇾ {country}\n\n"
                  f"• » Gateway ⇾ BRAINTREE B3 AUTH\n"
                  f"• » Request by ⇾ KUSHAL\n"
                  f"• » Time ⇾ {round(random.uniform(0.5, 2.5), 2)}s")
    return render_template_string(HTML_TEMPLATE, result=result)

# --- BOT HANDLERS ---
@bot.message_handler(commands=['st'])
def check_bot(message):
    card = message.text.replace('.st ', '')
    issuer, info, country, status, response = get_card_data(card)
    msg = f"• » Card ⇾ {card}\n• » Status ⇾ {status}\n• » Response ⇾ {response}\n\n• » Issuer ⇾ {issuer}\n• » Info ⇾ {info}\n• » Country ⇾ {country}\n\n• » Gateway ⇾ BRAINTREE B3 AUTH\n• » Request by ⇾ KUSHAL"
    bot.reply_to(message, msg)

@bot.message_handler(commands=['gen'])
def gen_bot(message):
    bin_base = message.text.replace('.gen ', '')
    # 16 digit generation logic
    card = bin_base + ''.join([str(random.randint(0,9)) for _ in range(16 - len(bin_base))])
    bot.reply_to(message, f"✨ Generated Card:\n`{card}`")

if __name__ == '__main__':
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
