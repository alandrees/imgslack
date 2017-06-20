"""
Copyright 2017 Pirate Hour Records

Author: Alan Drees

Purpose: Implement the queue worker process for ImgSlack
"""

import requests
import json
import pprint
import greenstalk
import os
import uuid

import ImgSlackConfig

app_config = ImgSlackConfig.load_config()

team_config = {}

exit_loop = False

def pp(data):
    """
    Wrapper around pretty print to print stuff to stdout

    @param data (mixed) any data structure to be printed nicely

    @returns None
    """
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)

def process_image_queue():
    """
    Queue worker entrypoint

    @param None

    @returns None
    """
    global team_config

    host = app_config['beanstalk']['host']
    port= app_config['beanstalk']['port']
    stalk = greenstalk.Client()

    while not exit_loop:
        jid, body = stalk.reserve()

        body = tuple(json.loads(body))

        team_config = app_config['teams'][body[1]]

        metadata = get_data(body[0])

        if metadata is not False:
            image = download_image(metadata)
            metadata['local_path'] = image

            for channel in metadata['channels']:
                notify_channel(channel[1],
                                   generate_link(image))

        print(body[0] + " complete")
        stalk.delete(jid)

    stalk.close()
    exit

def get_data(fileid):
    """
    Builds an image metadata object

    @param fileid (string) fileid to get the metadata for

    @returns (dict) Metadata fields aggregated together
    """
    img = get_image_data(fileid)

    if not img['mimetype'].startswith('image/'):
        return False

    channels = []

    for channel in img['channels']:
        channel_info = get_channel_data(channel)
        channel_info = (channel, channel_info['channel']['name'])
        channels.append(channel_info)

    img['channels'] = channels

    user_data = get_user_data(img['user'])['user']

    img['user'] = (user_data['id'], user_data['name'])
    team_data = get_team(user_data['team_id'])['team']
    img['team'] = (user_data['team_id'], team_data['domain'], team_data['name'])

    return img

def get_image_data(fileid):
    """
    Make a call to the slack API method files.info

    @param fileid (string) slack file id to lookup

    @returns (dict) dictionary of file metadata
    """
    data = {'file' : fileid}

    api_result  = make_api_call('files.info', data)

    return json.loads(api_result.text)['file']

def get_channel_data(channel):
    """
    Make a call to the slack API method channels.info

    @param channel (string) slack channel id to lookup

    @returns (dict) dictionary of channel metadata
    """
    data = {'channel' : channel}

    api_result = make_api_call('channels.info', data)

    return json.loads(api_result.text)

def get_user_data(user):
    """
    Make a call to the slack API method users.info

    @param user (string) slack user id to lookup

    @returns (dict) dictionary of user metadata
    """
    data = {'user' : user}

    api_result = make_api_call('users.info', data)

    return json.loads(api_result.text)

def get_team(teamid):
    """
    Make a call to the slack API method team.info

    @param teamid (string) slack team id to lookup

    @returns (dict) dictionary of team metadata
    """
    data = {}

    api_result = make_api_call('team.info', data)

    return json.loads(api_result.text)


def make_api_call(method, data):
    """
    Lower level function to make a call to the slack api

    @param method (string) Slack API method to call
    @param data (dict) fields to be passed to the slack API

    @returns (Request Response) the API's response
    """
    if 'token' not in data:
        data = data.copy()

        data.update({'token': team_config['oauth_token']})

    req = requests.post(app_config['workers']['api_url'] + method, data)

    return req

def download_image(img):
    """
    Download the image to the location specified in the config file

    @param img (dict) dictionary containing the image's metadata

    @returns (string) contains the local filename generated for the file
    """
    filename = uuid.uuid4().hex + '.' + img['filetype']
    url = img['url_private_download']
    file_path = app_config['workers']['file_target'] + '/' + img['team'][0]

    if not os.path.isdir(file_path):
        os.mkdir(file_path)

    local_filename = file_path + '/' + filename

    # NOTE the stream=True parameter

    authorization_field = 'Bearer ' + team_config['oauth_token']

    request_header = {'Authorization' : authorization_field}

    r = requests.get(url,
                     stream=True,
                     headers=request_header)

    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

    return local_filename

def generate_link(path):
    """
    Build the external link to the file

    @param path (string) absolute path to the file (including 'file_target')

    @returns (string) usable external URL to the image file
    """
    return app_config['workers']['external_url'] + \
      path.replace(app_config['workers']['file_target'], '')

def notify_channel(channel, link):
    """
    Send a message to the channel where the image was originally shared

    @param channel (string) channel to which the link was originally shared
    @param link (string) link to post to the channel

    @returns (boolean)
    """

    channel = '#' + channel

    notify_user = app_config['workers']['notify_user']

    data = {'channel'      : channel,
            'text'         : link,
            'token'        : team_config['bot_token'],
            'username'     : notify_user,
            'unfurl_media' : 'false'}


    api_result = make_api_call('chat.postMessage', data)

    message_result = json.loads(api_result.text)

    return message_result['ok']

if __name__ == '__main__':
    process_image_queue()
