import os
from flask import Flask, render_template

app = Flask(__name__)

# Dummy products data (Isse baad mein MongoDB se replace kar lena)
products = {
    "google_play": [
        {"id": 1, "name": "₹ 10 Google Code", "price": 10},
        {"id": 2, "name": "₹ 100 Google Code", "price": 100}
    ],
    "gaming": [
        {"id": 3, "name": "FF Weekly Membership", "price": 89},
        {"id": 4, "name": "100 Diamonds", "price": 80}
    ]
}

@app.route('/')
def index():
    return render_template('index.html', products=products)

if __name__ == '__main__':
    # Render ke liye port dynamic rakha hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
