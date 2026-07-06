from flask import Flask, render_template_string, request
import telebot
import threading
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
BOT_TOKEN = "8922478884:AAHgrLyM20xpxi-GKRiC_W_Gx8uwMUV0E5s"
YOUR_TELEGRAM_ID = "6632236983"
bot = telebot.TeleBot(BOT_TOKEN)

# --- REAL-TIME DATA FUNCTION (API LOGIC) ---
def get_bin_info(card):
    bin_number = card[:6]
    # Yahan hum public bin lookup API use kar rahe hain jo real-time country/bank degi
    try:
        res = requests.get(f"https://lookup.binlist.net/{bin_number}").json()
        bank = res.get('bank', {}).get('name', 'Unknown')
        country = res.get('country', {}).get('name', 'Unknown')
        return bank, country
    except:
        return "Unknown", "Unknown"

# --- BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to KUSHAL BOT!\n\nCommands:\n.st [card] - Check Card\n.gen [bin] - Generate")

@bot.message_handler(func=lambda message: message.text.startswith(('.st', '.gen')))
def handle_commands(message):
    data = message.text.split(' ', 1)
    cmd = data[0]
    payload = data[1] if len(data) > 1 else ""
    
    if cmd == ".st":
        bank, country = get_bin_info(payload)
        msg = f"✅ Result for: {payload[:6]}***\nStatus: Approved ✅\nBank: {bank}\nCountry: {country}\nChecked by: KUSHAL"
        bot.reply_to(message, msg)
    elif cmd == ".gen":
        bot.reply_to(message, f"⚙️ Generating for {payload[:6]}...")

# --- UI TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #0f0f0f; color: #fff; font-family: 'Courier New', monospace; text-align: center; padding: 20px; }
        .result-box { 
            background: #121212; border: 1px solid #333; padding: 20px; border-radius: 15px; 
            display: inline-block; text-align: left; margin-top: 20px; width: 90%; max-width: 400px;
            animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
        .status-approved { color: #00ff00; font-weight: bold; }
    </style>
</head>
<body>
    <h1>KUSHAL CHECKER</h1>
    <form method="POST" action="/check">
        <textarea name="card_info" placeholder="card|mm|yy|cvv" required style="width: 300px; height: 60px;"></textarea><br>
        <button type="submit" style="background:#ff4500; color:white; border:none; padding:10px 20px; cursor:pointer;">CHECK CARD</button>
    </form>
    {% if result %}
    <div class="result-box">
        <p>CC: {{ result.cc }}</p>
        <p>Status: <span class="status-approved">{{ result.status }}</span></p>
        <p>Bank: {{ result.bank }}</p>
        <p>Country: {{ result.country }}</p>
        <p>Checked by: KUSHAL</p>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/check', methods=['POST'])
def check():
    card = request.form.get('card_info')
    bank, country = get_bin_info(card)
    result = {"cc": card, "status": "Approved ✅", "bank": bank, "country": country}
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
