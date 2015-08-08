# coding=utf-8
from __future__ import print_function

from .. import config
from ..helpers.mailer import mailer


def send_auth_email(user, subject, msg):
    try:
        mailer.send(
            subject=subject,
            from_email=config.MAILER_FROM,
            to=user.email,
            html=msg
        )
    except Exception as e:
        print(e)
