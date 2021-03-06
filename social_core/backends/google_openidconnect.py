"""
Google OpenIdConnect:
    https://python-social-auth.readthedocs.io/en/latest/backends/google.html
"""
from .open_id_connect import OpenIdConnectAuth
from django.conf import settings

class GoogleOpenIdConnect(OpenIdConnectAuth):
    name = 'google-openidconnect'
    OIDC_ENDPOINT = 'https://accounts.google.com'
    # differs from value in discovery document
    # http://openid.net/specs/openid-connect-core-1_0.html#rfc.section.15.6.2
    ID_TOKEN_ISSUER = 'https://accounts.google.com'

    def __init__(self, *args, **kwargs):
        super(GoogleOpenIdConnect, self).__init__(*args, **kwargs)

        # TODO: When time allows, find out what the setting actually should be called so
        # We don't need this horrible hack.
        self._orig_setting = self.setting
        self.setting = self.my_setting_hack

    def my_setting_hack(self, name, default=None):
        if name == 'SECRET' or name == 'ID_TOKEN_DECRYPTION_KEY':
            return settings.SOCIAL_AUTH_GOOGLE_OPENIDCONNECT_SECRET
        elif name == 'KEY':
            return settings.SOCIAL_AUTH_GOOGLE_OPENIDCONNECT_KEY
        else:
            return self._orig_setting(name, default)
