"""Keeping myself safe with a little security."""
import os

from passlib.apps import custom_app_context as pwd_context

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow
from pyramid.security import Authenticated, Everyone


def includeme(config):
    """Set authentification priority."""
    auth_secret = os.environ.get('AUTH_SECRET', '')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('view')
    config.set_root_factory(MyRoot)


def is_authenticated(username, password):
    """Check if username and password match environment data."""
    stored_username = os.environ.get('AUTH_USERNAME', '')
    hashed_password = os.environ.get('AUTH_PASSWORD', '')
    is_authenticated = False
    if stored_username and hashed_password:
        if username == stored_username:
            try:
                is_authenticated =\
                    pwd_context.verify(password, hashed_password)
            except ValueError:
                pass
    return is_authenticated


class MyRoot(object):
    """Define premissions for config routes."""

    def __init__(self, request):
        """Initialize request permission."""
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'secret'),
    ]
