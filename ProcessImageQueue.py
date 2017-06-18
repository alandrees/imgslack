import requests
import json
import pprint
import greenstalk
import os
import uuid

oauth_token = \
  'xoxp-126494226213-125700289296-199373791090-7f75eb64ea4de22a88b8641a60c03c73'
bot_token = 'xoxb-198714945568-DAtYfMJ2YPkJp2hT8yr5Fa8p'
api_url = 'https://slack.com/api/'
file_target = '/var/www/slack.pirate-hour.net/public'
external_url = 'http://slack.pirate-hour.net.webdev'
notify_user = 'ircimageservice'

exit_loop = False

def process_image_queue():
    stalk = greenstalk.Client()

    while not exit_loop:
        jid, body = stalk.reserve()

        metadata = get_data(body)

        if metadata is not False:
            image = download_image(metadata)
            metadata['local_path'] = image
            push_to_database(metadata)

            for channel in metadata['channels']:
                notify_channel(channel[1],
                                   generate_link(image))

        stalk.delete(jid)

    stalk.close()

def get_data(fileid):
    img = get_image_data(fileid)

    if not img['mimetype'].startswith('image/'):
        return False

    channels = []

    for channel in img['channels']:
        channel_info = get_channel_data(channel)
        channel_info = (channel, channel_info['channel']['name'])
        channels.append(channel_info)

    img['channels'] = channels

    img['user'] = get_user_data(img['user'])['user']['name']
        
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(img)


def get_image_data(fileid):
    data = {'file' : fileid}

    api_result  = make_api_call('files.info', data)

    return json.loads(api_result.text)['file']

def get_channel_data(channel):

    data = {'channel' : channel}
        
    api_result = make_api_call('channels.info', data)

    return json.loads(api_result.text)


def get_user_data(user):

    data = {'user' : user}

    api_result = make_api_call('users.info', data)

    return json.loads(api_result.text)
        
def download_img(img):
    pass

def make_api_call(method, data):
    data = data.copy()
    data.update({'token': oauth_token})

    req = requests.post(api_url + method, data)

    return req
