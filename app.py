from flask import Flask, render_template

app = Flask(__name__)

products = [
    {"name": "100 Google Play", "price": 12000, "image": "play100.png"},
    {"name": "100 Diamonds", "price": 1000, "image": "diamonds.png"},
    {"name": "Booyah Pass", "price": 15000, "image": "booyah.png"},
    {"name": "50 Google Play", "price": 6000, "image": "play50.png"},
    {"name": "FF Membership", "price": 8500, "image": "ff_membership.png"},
    {"name": "Amazon Rs 20", "price": 500, "image": "amazon.png"}
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
