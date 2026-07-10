import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import string, random
from dotenv import load_dotenv

# Load variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'kushal_secret_key_2026'

# Setup
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# MongoDB Connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client['shortener_db']
users_col = db['users']
urls_col = db['links']

class User(UserMixin):
    def __init__(self, email): self.id = email

@login_manager.user_loader
def load_user(email): return User(email)

# --- ROUTES ---

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('admin@kushal.com')
        password = request.form.get('123456')
        user_data = users_col.find_one({'_id': email})
        if user_data and bcrypt.check_password_hash(user_data['password'], password):
            login_user(User(user_data['_id']))
            return redirect(url_for('dashboard'))
        return "Invalid Credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not users_col.find_one({'_id': email}):
            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
            users_col.insert_one({'_id': email, 'password': hashed_pw})
            return redirect(url_for('login'))
        return "Email already exists!", 400
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        long_url = request.form.get('url')
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        urls_col.insert_one({'code': code, 'original': long_url, 'user': current_user.id})
    user_links = list(urls_col.find({'user': current_user.id}))
    return render_template('dashboard.html', links=user_links)

@app.route('/<short_code>')
def redirect_url(short_code):
    data = urls_col.find_one({'code': short_code})
    return redirect(data['original']) if data else "Link not found", 404

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
