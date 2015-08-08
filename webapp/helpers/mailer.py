# coding=utf-8
import logging

import mailshake
from mailshake.message import EmailMessage

from .. import config


MailerClass = getattr(mailshake, config.MAILER_CLASS)
mailer = MailerClass(**config.MAILER_SETTINGS)


def send_email(onsent=None, onerror=None, *args, **kwargs):
    """Centralize the email sending
    """
    logger = logging.getLogger(__name__)
    kwargs.setdefault('from_email', config.MAILER_FROM)
    email_msg = EmailMessage(*args, **kwargs)

    try:
        logger.debug(u'EMAIL to {}'.format(
            ', '.join(email_msg.get_recipients() or [])
        ))
    except Exception:
        pass
    try:
        mailer.send_messages(email_msg)
        if onsent:
            onsent()
    except Exception as e:
        logger.error(str(e))
        if onerror:
            onerror(e)
