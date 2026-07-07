from flask import Flask, render_template

app = Flask(__name__)

# Aapke saare products list
products = [
    {"name": "100 Google Play", "price": 12000, "image": "https://i.imgur.com/example1.png"},
    {"name": "100 Diamonds", "price": 1000, "image": "https://i.imgur.com/example2.png"},
    {"name": "Booyah Pass", "price": 15000, "image": "https://i.imgur.com/example3.png"},
    {"name": "50 Google Play", "price": 6000, "image": "https://i.imgur.com/example4.png"},
    {"name": "FF Membership", "price": 8500, "image": "https://i.imgur.com/example5.png"},
    {"name": "Amazon Pay 20", "price": 500, "image": "https://i.imgur.com/example6.png"},
    {"name": "10 Google Code", "price": 1500, "image": "https://i.imgur.com/example7.png"}
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/logout')
def logout():
    return "Logged out successfully!"

if __name__ == '__main__':
    app.run(debug=True)
