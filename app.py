import os
from flask import Flask, render_template

app = Flask(__name__)

# Yeh line Render ke liye zaroori hai
# Agar PORT environment variable set hai toh use use karega, 
# warna default 5000 par chalega
port = int(os.environ.get("PORT", 5000))

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Render ke liye host '0.0.0.0' hona chahiye
    app.run(host='0.0.0.0', port=port)
