import requests


class CloudbrainAuth(object):
    def __init__(self, base_url=None, token=None):
        self.base_url = base_url or 'http://dockerhost:3000'
        self.token = token or ''

    def token_info(self, token=None):
        token_url = self.base_url + '/oauth/token/info'
        token = token or self.token

        headers = {
            'Authorization': 'Bearer %s' % token
        }

        response = requests.get(token_url, headers=headers, verify=False)
        return response.json()

    def vhost_by_token(self, token=None):
        info_url = self.base_url + '/rabbitmq/vhost/info'
        token = token or self.token

        headers = {
            'Authorization': 'Bearer %s' % token
        }

        response = requests.get(info_url, headers=headers, verify=False)
        return response.json()

    def vhost_by_username(self, username=None):
        info_url = self.base_url + '/rabbitmq/vhost/info'

        headers = {}
        body = {
            "username": username
        }

        response = requests.post(info_url, data=body, headers=headers,
                                 verify=False)
        return response.json()

    def get_vhost_by_token(self, token):
        response = self.vhost_by_token(token=token)
        return response['vhost']

    def get_vhost_by_username(self, username):
        response = self.vhost_by_username(username=username)
        return response['vhost']
