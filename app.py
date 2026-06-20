import os
from flask import Flask, render_template, request, redirect, url_for, session

# Path setup: current directory ko base manna
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, 
            template_folder=os.path.join(basedir, 'templates'),
            static_folder=os.path.join(basedir, 'static'))

app.secret_key = 'secret123'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    player_id = request.form.get('playerId')
    session['user_id'] = player_id
    return redirect(url_for('verify'))

@app.route('/verify')
def verify():
    return render_template('verify.html', player_id=session.get('user_id', 'Guest'))

@app.route('/shop')
def shop():
    return render_template('shop.html')

if __name__ == '__main__':
    app.run()
