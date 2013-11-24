import json

import requests


class PostNotification(object):

    def __init__(self, url):
        self.url = url

    def send(self, payload):
        headers = {'content-type': 'application/json'}
        r = requests.post(self.url, data=json.dumps(payload), headers=headers)
