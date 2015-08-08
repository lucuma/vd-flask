# coding=utf-8
from __future__ import print_function

import getpass

import baker


def prompt(text, default=None, _test=None):
    """Ask a question via raw_input() and return their answer.

    param text: prompt text
    param default: default value if no answer is provided.
    """

    text += ' [{0}]'.format(default if default else '')
    while True:
        if _test is not None:
            print(text)
            resp = _test
        else:
            resp = raw_input(text)
        if resp:
            return resp
        if default is not None:
            return default


def prompt_pass(text, default=None, _test=None):
    """Prompt the user for a secret (like a password) without echoing.

    :param name: prompt text
    :param default: default value if no answer is provided.
    """

    text += ' [{0}]'.format(default if default else '')
    while True:
        if _test is not None:
            print(text)
            resp = _test
        else:
            resp = getpass.getpass(text)
        if resp:
            return resp
        if default is not None:
            return default


@baker.command
def create_user(login, passw, **data):
    """Creates a new user.
    """
    from ..database import db
    from .models.auth import auth, User

    password_minlen = auth.password_minlen
    while len(passw) < password_minlen:
        print('Password is too short (min {0} chars).'.format(password_minlen))
        passw = prompt_pass('>>> Password? (typing will be hidden)')

    login = unicode(login)
    passw = unicode(passw)
    u = User(login=login, email=login, password=passw, **data)
    db.add(u)
    db.commit()
    print('Created user `{0}` with password `{1}`.'.format(login, passw))
    print('To change the password use `manage.py change_password {0}`'.format(login))
    print('To change the email use `manage.py update_user {0} email=mynew@email`'.format(login))


@baker.command
def change_password(login, passw=None):
    """Changes the password of an existing user."""
    from ..database import db
    from .models.auth import auth, User

    login = unicode(login)
    user = User.by_login(login)
    if not user:
        print('User not found')
        return

    if passw is None:
        passw = prompt_pass('>>> Password? (typing will be hidden)')

    password_minlen = auth.password_minlen
    while len(passw) < password_minlen:
        print('Password is too short (min {0} chars).'.format(password_minlen))
        passw = prompt_pass('>>> Password? (typing will be hidden)')

    passw = unicode(passw)
    user.password = passw
    db.commit()
    print('Changed the password of user `{0}`.'.format(login.encode('utf8')))


@baker.command
def update_user(login, **data):
    """Updates the data of an existing user."""
    from ..database import db
    from .models.auth import User

    login = unicode(login)
    user = User.by_login(login)
    if not user:
        print('User `{0}` not found.'.format(login.encode('utf8')))
        return

    for key, val in data.items():
        setattr(user, key, val)
    db.commit()
    print('User `{0}` updated.'.format(login.encode('utf8')))


@baker.command
def add_role(login, role):
    """Adds a role to the user
    """
    from ..database import db
    from .models.auth import User

    login = unicode(login)
    role = unicode(role)
    user = User.by_login(login)
    if not user:
        print('User `{0}` not found.'.format(login.encode('utf8')))
        return
    user.add_role(role)
    db.commit()
    print('User `{0}` has now the `{1}` role.'.format(
        login.encode('utf8'), role.encode('utf8')))


@baker.command
def remove_role(login, role):
    """Remove a role from the user
    """
    from ..database import db
    from .models.auth import User

    login = unicode(login)
    role = unicode(role)
    user = User.by_login(login)
    if not user:
        print('User `{0}` not found.'.format(login.encode('utf8')))
        return
    user.remove_role(role)
    db.commit()
    print('User `{0}` no longer has the `{1}` role.'.format(
        login.encode('utf8'), role.encode('utf8')))
