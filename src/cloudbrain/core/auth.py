import requests
import json


class CloudbrainAuth(object):
    def __init__(self, auth_url):
        """
        :param auth_url: (str)
            Cloudbrain authentication server URL.
            It's recommended to use ``cloudbrain.core.config.get_config()`` to
            pass the correct URL value.
        """
        self.auth_url = auth_url

    def get_user_token_by_credentials(self, username, password):
        """
        This is the OAuth 2.0 grant used to request an id_token.

        :param username: (str)
            User name or email.
        :param password: (str)
            User password.
        :return: (request.Response)
            Response contains access_token, id_token, scopes, and token_type.
        """
        url = self.auth_url + '/user/token'
        body = {
            "username": username,
            "password": password
        }
        return requests.post(url, data=json.dumps(body), verify=False)

    def get_user_info_by_token(self, id_token):
        """
        Return a user profile based on the user's token_id.

        :param id_token: (str)
            User's ID token.
        """
        url = self.auth_url + '/user/info'
        body = {
            "id_token": id_token
        }
        return requests.post(url, data=json.dumps(body), verify=False)

    def get_vhost(self, username_or_token, password):
        """
        Returns a vhost based on the username and password. Note that the
        token can passed in place of the username - in this case, the password
        is set to an empty string.

        :param username_or_token: (str)
            User name or user token.
        :param password: (str)
            User password or empty string if the token is passed.
        :return vhost: (str)
            RabbitMQ virtual host.
        """
        if password:
            vhost = self.get_vhost_by_username(username_or_token)
        else:
            vhost = self.get_vhost_by_token(username_or_token)
        return vhost

    def get_vhost_by_token(self, id_token):
        """
        Get the vhost based on the user token.
        """
        vhost_info_url = '%s/vhost/info?id_token=%s' % (self.auth_url,
                                                        id_token)

        response = requests.get(vhost_info_url, verify=False)
        return self._parse_vhost_response(response)

    def get_vhost_by_username(self, username):
        """
        Get the vhost based on the username.
        """
        vhost_info_url = '%s/vhost/info?email=%s' % (self.auth_url,
                                                     username)

        response = requests.get(vhost_info_url, verify=False)
        return self._parse_vhost_response(response)

    @staticmethod
    def _parse_vhost_response(response):
        if response.status_code == 200:
            json_response = response.json()
            if 'vhost' in json_response:
                return json_response['vhost']
            else:
                raise RuntimeError('No "vhost" was found in the response.')
        else:
            raise RuntimeError('Unable to get "vhost". Server responded '
                               'with status code: %s' % response.status_code)
