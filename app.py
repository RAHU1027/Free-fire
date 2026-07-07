@app.route('/')
def index():
    # MongoDB se data fetch karein
    play_codes = db.products.find({'category': 'google_play'})
    others = db.products.find({'category': 'gaming'})
    return render_template('index.html', play_codes=play_codes, others=others)
