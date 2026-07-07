from flask import Flask, render_template

# 1. Sabse pehle Flask instance create karein
app = Flask(__name__)

# 2. Ab decorators ka use karein
@app.route('/')
def index():
    return render_template('index.html')

# 3. Last mein app run karein
if __name__ == '__main__':
    app.run(debug=True)
