from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required
from pymongo import MongoClient
import requests
import threading
import time
import string
import random

app = Flask(__name__)
app.secret_key = 'kushal_secret_key'

# MongoDB Config
client = MongoClient("YOUR_MONGODB_CONNECTION_STRING_HERE")
db = client['shortener_db']
urls = db['links']
users = db['users']

# 24/7 Uptime Ping Function
def keep_alive():
    while True:
        try:
            # Apne domain ka URL yaha daal dena
            requests.get("https://your-app-name.onrender.com") 
        except:
            pass
        time.sleep(300) # Har 5 minute mein ping

threading.Thread(target=keep_alive, daemon=True).start()

# Helper: Short Code Generator
def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['url']
        short_code = generate_code()
        urls.insert_one({'original': long_url, 'code': short_code})
        return f"Short Link: yourdomain.com/{short_code}"
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_url(short_code):
    data = urls.find_one({'code': short_code})
    return redirect(data['original']) if data else "Link not found"

if __name__ == '__main__':
    app.run(debug=True)
