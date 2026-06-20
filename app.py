from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey' # Session ke liye zaroori hai

# Demo valid IDs (Aap yahan apni valid IDs ki list daal sakte hain)
VALID_IDS = ['1234567890', '9876543210'] 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    player_id = request.form.get('playerId')
    # Check karein ki ID valid list mein hai ya nahi
    if player_id in VALID_IDS:
        session['user_id'] = player_id
        return redirect(url_for('verify'))
    else:
        return "Invalid Player ID! Please try again."

@app.route('/verify')
def verify():
    if 'user_id' in session:
        return render_template('verify.html', player_id=session['user_id'])
    return redirect(url_for('index'))

@app.route('/shop')
def shop():
    return render_template('shop.html')

if __name__ == '__main__':
    app.run(debug=True)
