from flask import Flask, render_template

# 1. Initialize Flask app
app = Flask(__name__)

# 2. Main route (Homepage)
@app.route('/')
def index():
    # 'index.html' aapke 'templates' folder mein honi chahiye
    return render_template('index.html')

# 3. Server run configuration
if __name__ == '__main__':
    # host='0.0.0.0' aur port 5000 set kiya hai
    # debug=True se aapko errors turant pata chal jayenge
    app.run(host='0.0.0.0', port=5000, debug=True)
