"""
Copyright 2017 Pirate Hour Productions

Author: Alan Drees

Purpose: Flask-enabled http endpoints for recieving events from slack
and adding the image to queue job
"""

import yaml
from flask import Flask
from flask import request
from flask import jsonify
import greenstalk

app = Flask(__name__)

app_token = 'oeZ8mFbswzdGBnLpEbcvxT4v'

@app.route('/status/', methods=['GET'])
def status():
    """
    Route Function for handling the queue status page

    @param None

    @returns Json Response containing the greenstalk stats
    """
    stalk = greenstalk.Client()
    stats = stalk.stats()
    return jsonify(stats)


@app.route('/image/<team>', methods=['POST'])
def image_event(team):
    """
    Route Function for handling the image event, and push it to the queue

    @param team (string) team to which this image belongs

    @returns Json Response containing the keypair {'jerb' : jobid}
    """
    image_id = request.json['event']['file']['id']

    if app_token == request.json['token']:
            stalk = greenstalk.Client()
            jobid = stalk.put(image_id)
            stalk.close()

    return jsonify([])
