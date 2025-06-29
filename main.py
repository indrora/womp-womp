import io
from flask import Flask, request, jsonify, render_template, g, send_file
import os
from card import Troublecard, split_card
from storage import Cardfile
from render import CardRenderer

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_prefixed_env("SCC")

# Basic front page
@app.route('/')
def index():
    return render_template('index.html')

# List of current cards.
@app.route('/cards/', methods=['GET'])
def list_cards():
    db = get_db()
    after = request.args.get('after', None)
    cards = list(db.page(after=after))
    nextpage = cards[-1].id if len(cards) == 10 else None
    return render_template('card_list.html', cards=cards, cursor=nextpage )

# Show an individual card
@app.route('/cards/<card_id>', methods=['GET'])
def get_card(card_id):
    db = get_db()
    card = db.get(card_id)
    if card:
        return render_template('show_card.html', card=card)
    else:
        return "Not Found", 404

# Render a card to a PNG image.
@app.route('/cards/<card_id>.png')
def get_card_image(card_id):
    db = get_db()
    card = db.get(card_id)
    if card:
        renderer = CardRenderer(app.config['ASSET_PATH'])
        img = renderer.render_card(card)
        imgio = io.BytesIO()
        img.save(imgio, format='PNG')
        imgio.seek(0)
        return send_file(imgio, mimetype='image/png')
    else:
        return send_file(os.path.join(app.config['ASSET_PATH'], 'front.png'), mimetype='image/png')


#
# Get a database connection. This abuses the Flask app context to store the connection to the database.
#
def get_db() -> Cardfile:
    if not 'cardfile' in app.config:
        app.config['cardfile'] = Cardfile(app.config['CARDFILE_PATH'])
    return app.config['cardfile']

# card intake function.

@app.route('/card', methods=['POST'])
def create_card():
    # Get the cardfile database
    cardfile = get_db()
    # If we're too large, reject it
    if request.content_length > 4096* 1024:  # Limit to 4MB
        return jsonify({"error": "Card data too large"}), 413
    
    # Get the card data
    card_block = request.get_data(as_text=True)
    if not card_block:
        return jsonify({"error": "No card data provided"}), 400

    # load the card data into a real troublcard object
    # This splits the card data into a series of integers
    card_data = split_card(card_block)
    # And this parses those integers into a troublecard object
    card = Troublecard.from_raw(card_data)
    # insert the card into the database
    id = cardfile.insert(card)
    # Return the id of the card and a 201 Created response
    return jsonify({"id": id}), 201


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
