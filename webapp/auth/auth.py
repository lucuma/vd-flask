# coding=utf-8
from authcode import Auth, setup_for_flask

from .. import config
from ..app import app
from ..database import db
from ..models.user_mixin import UserMixin

from .helpers import send_auth_email


auth = Auth(config.SECRET_KEY, db=db, UserMixin=UserMixin, roles=True,
            **config.AUTH_SETTINGS)

User = auth.User
Role = auth.Role

setup_for_flask(auth, app, send_email=send_auth_email)
