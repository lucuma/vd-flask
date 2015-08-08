# coding=utf-8
from flask import g, session


LOCAL_FLASHES = '_fm'


def flash(msg, cat='info', **kwargs):
    """Flashes a message to the next session.  In order to remove the
    flashed message from the session and to display it to the user,
    the view has to call `shake.get_messages`.

    msg
    :   the message to be flashed.
    cat
    :   optional classification of the message. By default is 'info'.
    kwargs
    :   extra data passed along the message

    """
    kwargs['msg'] = msg
    kwargs['cat'] = cat
    session.setdefault(LOCAL_FLASHES, []).append(kwargs)


def get_flashed_messages():
    """Pulls all flashed messages from the session and returns them.
    Further calls in the same request to the function will return
    the same messages.
    """
    flashes = getattr(g, LOCAL_FLASHES, None)
    if not flashes:
        flashes = session.get(LOCAL_FLASHES) or []
        setattr(g, LOCAL_FLASHES, flashes)
        if flashes:
            del session[LOCAL_FLASHES]
    return flashes or []
