import yaml
from flask import Flask
from flask import request
from flask import jsonify
import greenstalk

import SlackImageEventController

app = Flask(__name__)

app_token = 'oeZ8mFbswzdGBnLpEbcvxT4v'

@app.route('/status/', methods=['GET'])
def status():
    stalk = greenstalk.Client(host='127.0.0.1', port=11300)
    stats = stalk.stats()
    return jsonify(stats)

@app.route('/', methods=['GET'])
def root():
    return "I think i'm getting the fear..."

@app.route('/image/<id>', methods=['GET'])
def team(id):
    return "The image id you're looking for is: " + id

@app.route('/image', methods=['POST'])
def image_event():
    if app_token == request.json['token']:
        SlackImageEventController.get_data(request.json['event']['file'])
    return jsonify([])
