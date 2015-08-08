# coding=utf-8
from __future__ import print_function

from webapp.database import db
from webapp.auth import User


def load_users():
    print('Loading users...')
    USERS = [
        {
            'login': u'admin',
            'password': u'admin',
            'name': u'Super Admin',
            'email': u'admin@example.com',
            'roles': [u'admin'],
        }
    ]
    for data in USERS:
        if '_' in data:
            del data['_']
        if User.by_login(data['login']):
            continue

        roles = data.pop('roles', [])

        user = User(**data)
        db.add(user)

        for role in roles:
            user.add_role(role)
    db.commit()
