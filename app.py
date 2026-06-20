from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connect karein
def get_db():
    conn = sqlite3.connect('users.db')
    return conn

# Database table setup (sirf ek baar chalana hai)
def init_db():
    conn = get_db()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY)')
    # 500+ IDs add karne ka logic ya loop yahan laga sakte hain
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    player_id = request.form.get('playerId')
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (player_id,)).fetchone()
    conn.close()
    
    if user:
        session['user_id'] = player_id
        return redirect(url_for('verify'))
    else:
        return "Invalid ID. 500+ members system mein ID nahi mili."

@app.route('/verify')
def verify():
    return render_template('verify.html', player_id=session.get('user_id'))

if __name__ == '__main__':
    app.run(debug=True)
