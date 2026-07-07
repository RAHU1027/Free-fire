import os
from flask import Flask, render_template

app = Flask(__name__)

# Aapka poora product menu data
products = [
    {"name": "FF Weekly Membership", "desc": "Garena Free Fire (Once in 2 Weeks)", "tag": "instant", "price": 8500, "image": "ff_membership.png"},
    {"name": "Booyah Premium Pass", "desc": "Garena Free Fire (Once in 2 Week)", "tag": "instant", "price": 15000, "image": "booyah_pass.png"},
    {"name": "₹ 10", "desc": "Google Play Gift Card (Once a Month)", "tag": "popular", "price": 1000, "image": "play_store.png"},
    {"name": "₹ 25", "desc": "Google Play Gift Card (Once a Month)", "tag": "popular", "price": 3000, "image": "play_store.png"},
    {"name": "₹ 50", "desc": "Google Play Gift Card (Once a Month)", "tag": "popular", "price": 6000, "image": "play_store.png"},
    {"name": "₹ 100", "desc": "Google Play Gift Card (Once a Month)", "tag": "popular", "price": 12000, "image": "play_store.png"},
    {"name": "100 Diamonds", "desc": "Free Fire MAX (Once A Month)", "tag": "instant", "price": 1000, "image": "diamonds.png"},
    {"name": "Amazon Pay Rs 20", "desc": "Amazon Pay Rs 20 (Once a Month)", "tag": "instant", "price": 500, "image": "amazon.png"},
    {"name": "₹ 10 Google Code", "desc": "Google Play Gift Card (Once a Month)", "tag": "instant", "price": 1500, "image": "play_store.png"}
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

if __name__ == '__main__':
    # Render aur local dono ke liye port setup
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
