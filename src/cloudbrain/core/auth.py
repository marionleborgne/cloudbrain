import requests
import json


class CloudbrainAuth(object):
    def __init__(self, rabbit_auth_url, auth0_base_url=None,
                 auth0_client_id=None, auth0_client_secret=None, token=None):
        """
        :param rabbit_auth_url: (str)
            RabbitMQ authentication server URL. E.g.: 'http://localhost:5000'
        :param auth0_base_url: (str)
            Auth0 URL. E.g.: 'https://yourdomain.auth0.com'
        :param auth0_client_id: (str)
            Auth0 client ID. Default is None.
        :param auth0_client_secret: (str)
            Auth0 client secret. Default is None.
        :param token: (str)
            Authentication token.
        """
        self.rabbit_auth_url = rabbit_auth_url
        self.auth0_base_url = auth0_base_url
        self.client_id = auth0_client_id
        self.client_secret = auth0_client_secret
        self.token = token
        if auth0_base_url:
            self.audience = '%s/api/v2/' % auth0_base_url
        else:
            self.audience = None

    def authorize_client(self):
        authorize_url = self.auth0_base_url + '/oauth/token'

        body = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience
        }

        return requests.post(authorize_url, data=body, verify=False)

    def authorize(self, username, password):
        authorize_url = self.auth0_base_url + '/oauth/token'

        body = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience,
            "username": username,
            "password": password,
            "scope": "openid"
        }

        return requests.post(authorize_url, data=body, verify=False)

    def get_user_by_email(self, client_token, email):
        get_user_url = '%susers?q=email:"%s"' % (self.audience,
                                                 email)
        headers = {
            "Authorization": "Bearer %s" % client_token,
            "Content-Type": "application/json"
        }

        return requests.get(get_user_url,
                            headers=headers,
                            verify=False)

    def get_user_id_by_email(self, client_token, email):
        r = self.get_user_by_email(client_token, email)
        response = r.json()
        if len(response) > 0:
            return response[0]['user_id']
        else:
            print('Invalid response: %s' % r)
            return None

    def patch_user(self, client_token, user_id, data):
        patch_user_url = self.audience + 'users/%s' % user_id

        headers = {
            "Authorization": "Bearer %s" % client_token,
            "Content-Type": "application/json"
        }

        return requests.patch(patch_user_url,
                              headers=headers,
                              data=json.dumps(data),
                              verify=False)

    def token_info(self, token=None):
        token_url = self.auth0_base_url + '/tokeninfo'
        token = token or self.token

        body = {
            "id_token": token
        }

        response = requests.post(token_url, data=body, verify=False)
        return response

    def token_by_credentials(self, username, password):
        response = self.authorize(username, password)
        return response.json()

    def vhost_by_token(self, token=None):
        vhost_info_url = '%s/vhost/info?id_token=%s' % (self.rabbit_auth_url,
                                                        token)

        return requests.get(vhost_info_url, verify=False)

    def vhost_by_username(self, username=None):
        vhost_info_url = '%s/vhost/info?email=%s' % (self.rabbit_auth_url,
                                                     username)

        return requests.get(vhost_info_url, verify=False)

    def get_vhost_by_token(self, token):
        response = self.vhost_by_token(token=token)
        return response.json()['vhost']

    def get_vhost_by_username(self, username):
        response = self.vhost_by_username(username=username)
        return response.json()['vhost']

    def get_vhost(self, rabbitmq_user, rabbitmq_pwd):
        if rabbitmq_pwd:
            rabbitmq_vhost = self.get_vhost_by_username(rabbitmq_user)
        else:
            rabbitmq_vhost = self.get_vhost_by_token(rabbitmq_user)
        return rabbitmq_vhost
