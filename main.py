from flask import Flask, request, jsonify, render_template, g 
import os

from storage import Cardfile
app = Flask(__name__)

app.config.from_prefixed_env("SCC")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cards/', methods=['GET'])
def list_cards():
    db = get_db()
    return jsonify({"cards":list(map(str, db.list_ids())) }), 200

@app.route('/cards/<card_id>', methods=['GET'])
def get_card(card_id):
    db = get_db()
    card = db.get(card_id)
    if card:
        return jsonify(card), 200
    else:
        return jsonify({"error": "Card not found"}), 404




def get_db() -> Cardfile:
    with app.app_context():
        if 'cardfile' not in g:
            g.cardfile = Cardfile(app.config['CARDFILE_PATH'])
        return g.cardfile

@app.after_request
def close_db(response):
    if 'cardfile' in g:
        g.cardfile.close()
        g.pop('cardfile', None)
    return response

@app.route('/card', methods=['POST'])
def create_card():
    cardfile = get_db()
    if request.content_length > 4096* 1024:  # Limit to 4MB
        return jsonify({"error": "Card data too large"}), 413
    
    card_data = request.get_data(as_text=True)
    if not card_data:
        return jsonify({"error": "No card data provided"}), 400

    card_id = cardfile.insert(card_data)
    return jsonify({"id": card_id}), 201



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
