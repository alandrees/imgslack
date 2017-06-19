"""
Copyright 2017 Pirate Hour Productions

Author: Alan Drees

Purpose: Flask-enabled http endpoints for recieving events from slack
and adding the image to queue job
"""

from flask import Flask
from flask import request
from flask import jsonify
import greenstalk
import json

import ImgSlackConfig

app = Flask(__name__)

app_token = 'oeZ8mFbswzdGBnLpEbcvxT4v'

app_config =  ImgSlackConfig.load_config()

@app.route('/status', methods=['GET'])
def status():
    """
    Route Function for handling the queue status page

    @param None

    @returns Json Response containing the greenstalk stats
    """

    host = app_config['beanstalk']['host']
    port = app_config['beanstalk']['port']

    stalk = greenstalk.Client(host, port)
    stats = stalk.stats()
    return jsonify(stats)


@app.route('/image/<team>', methods=['POST'])
def image_event(team):
    """
    Route Function for handling the image event, and push it to the queue

    @param team (string) team to which this image belongs

    @returns json response if it's a url_verification type, blank otherwise
    """
    if app_token == request.json['token']:
        if request.json['type'] == 'url_verification':
            return jsonify({'challenge' : request.json['challenge']})
        else:
            image_id = request.json['event']['file']['id']

            stalk = greenstalk.Client()
            jobid = stalk.put(json.dumps((image_id,team)))
            stalk.close()

            return ''
