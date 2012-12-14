"""
Google OpenID and OAuth support

OAuth works straightforward using anonymous configurations, username
is generated by requesting email to the not documented, googleapis.com
service. Registered applications can define settings GOOGLE_CONSUMER_KEY
and GOOGLE_CONSUMER_SECRET and they will be used in the auth process.
Setting GOOGLE_OAUTH_EXTRA_SCOPE can be used to access different user
related data, like calendar, contacts, docs, etc.

OAuth2 works similar to OAuth but application must be defined on Google
APIs console https://code.google.com/apis/console/ Identity option.

OpenID also works straightforward, it doesn't need further configurations.
"""
import json
from urllib import urlencode
from urllib2 import Request

from social.exceptions import AuthFailed
from social.backends.oauth import BaseOAuth2


class GoogleOAuth2(BaseOAuth2):
    """Google OAuth2 authentication backend"""
    name = 'google-oauth2'
    REDIRECT_STATE = False
    AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/auth'
    ACCESS_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
    DEFAULT_SCOPE = ['https://www.googleapis.com/auth/userinfo.email',
                     'https://www.googleapis.com/auth/userinfo.profile']
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('token_type', 'token_type', True)
    ]

    def get_user_id(self, details, response):
        """Use google email as unique id"""
        email = details['email']
        emails = self.strategy.setting('GOOGLE_WHITE_LISTED_EMAILS', [])
        domains = self.strategy.setting('GOOGLE_WHITE_LISTED_DOMAINS', [])
        if emails and email in emails:
            return  # you're good
        if domains and email.split('@', 1)[1] not in domains:
            raise AuthFailed(self, 'Domain not allowed')

        if self.strategy.setting('USE_UNIQUE_USER_ID', False):
            return response['id']
        else:
            return email

    def get_user_details(self, response):
        """Return user details from Orkut account"""
        email = response.get('email', '')
        return {'username': email.split('@', 1)[0],
                'email': email,
                'fullname': response.get('name', ''),
                'first_name': response.get('given_name', ''),
                'last_name': response.get('family_name', '')}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Google API"""
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        data = {'access_token': access_token, 'alt': 'json'}
        request = Request(url + '?' + urlencode(data))
        try:
            return json.loads(self.urlopen(request).read())
        except (ValueError, KeyError, IOError):
            return None


# Backend definition
BACKENDS = {
    'google-oauth2': GoogleOAuth2,
}