import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import string, random

app = Flask(__name__)
app.secret_key = 'kushal_secret_key'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client['shortener_db']
users_col = db['users']
urls_col = db['links']

class User(UserMixin):
    def __init__(self, email): self.id = email

@login_manager.user_loader
def load_user(email): return User(email)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        users_col.insert_one({'_id': email, 'password': password})
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = users_col.find_one({'_id': request.form['email']})
        if user_data and bcrypt.check_password_hash(user_data['password'], request.form['password']):
            login_user(User(user_data['_id']))
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        long_url = request.form['url']
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        urls_col.insert_one({'code': code, 'original': long_url, 'user': current_user.id})
    user_links = list(urls_col.find({'user': current_user.id}))
    return render_template('dashboard.html', links=user_links)

if __name__ == '__main__':
    app.run()
