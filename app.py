import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'kushal_super_secret_key'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# MongoDB setup with error handling
try:
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client['shortener_db']
    users_col = db['users']
    urls_col = db['links']
except Exception as e:
    print(f"DB Connection Error: {e}")

class User(UserMixin):
    def __init__(self, email): self.id = email

@login_manager.user_loader
def load_user(email): return User(email)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = users_col.find_one({'_id': email})
        if user and bcrypt.check_password_hash(user['password'], password):
            login_user(User(email))
            return redirect(url_for('dashboard'))
        return "Login Failed! Check credentials."
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
        return "Email already exists!"
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
