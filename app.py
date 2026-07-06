from flask import Flask, render_template_string, request
import telebot
import threading
import requests # Webservice ke liye import zaroori hai

app = Flask(__name__)

# --- CONFIGURATION ---
BOT_TOKEN = "8922478884:AAHgrLyM20xpxi-GKRiC_W_Gx8uwMUV0E5s"
YOUR_TELEGRAM_ID = "6632236983"
bot = telebot.TeleBot(BOT_TOKEN)

# --- BOT COMMANDS & WELCOME ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to KUSHAL BOT!\n\nCommands:\n.st - Check Card\n.gen - Generate Cards")

@bot.message_handler(commands=['st', 'gen'])
def handle_commands(message):
    bot.reply_to(message, f"⚙️ Command {message.text} received. Please enter details.")

# --- UI TEMPLATE WITH DESIGN & ANIMATION ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #0f0f0f; color: #fff; font-family: 'Courier New', monospace; text-align: center; padding: 20px; }
        textarea { width: 90%; max-width: 400px; height: 80px; background: #1a1a1a; color: #00ff00; border: 1px solid #333; margin: 10px 0; }
        button { background: #ff4500; color: white; padding: 10px 20px; border: none; cursor: pointer; border-radius: 5px; font-weight: bold; }
        
        /* Animation & Design */
        .result-box { background: #1a1a1a; border: 1px solid #333; padding: 20px; border-radius: 15px; display: inline-block; text-align: left; margin-top: 20px; width: 90%; max-width: 400px; animation: fadeIn 1s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .status-approved { color: #00ff00; font-weight: bold; }
    </style>
</head>
<body>
    <h1>KUSHAL CHECKER</h1>
    <form method="POST" action="/check">
        <textarea name="card_info" placeholder="card|month|year|cvv" required></textarea><br>
        <button type="submit">CHECK CARD</button>
    </form>
    {% if result %}
    <div class="result-box">
        <p>CC: {{ result.cc }}</p>
        <p>Status: <span class="status-approved">{{ result.status }}</span></p>
        <p>Response: {{ result.response }}</p>
        <p>Gateway: {{ result.gateway }}</p>
        <p>Bank: {{ result.bank }}</p>
        <p>Type: {{ result.type }}</p>
        <p>Country: {{ result.country }}</p>
        <p>Checked by: KUSHAL</p>
        <p>Credits left: {{ result.credits }}</p>
    </div>
    {% endif %}
</body>
</html>
"""

# --- WEBSERVICE LOGIC ---
def get_live_data(card):
    # Yahan apni API ka URL daalein
    # response = requests.get(f"YOUR_API_ENDPOINT?card={card}").json()
    # Mock data structure for testing:
    return {
        "cc": card, "status": "Approved ✅", "response": "Card added",
        "gateway": "Stripe", "bank": "Citibank N.A.", 
        "type": "Mastercard - Debit - Enhanced", "country": "United States 🇺🇸",
        "credits": "ID-8922"
    }

# --- ROUTES ---
@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/check', methods=['POST'])
def check():
    card = request.form.get('card_info')
    result = get_live_data(card)
    return render_template_string(HTML_TEMPLATE, result=result)

@app.route('/ping')
def ping():
    return "OK", 200

if __name__ == '__main__':
    # Background thread for bot
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    # Flask application
    app.run(host='0.0.0.0', port=5000)
