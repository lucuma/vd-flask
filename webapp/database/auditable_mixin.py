# coding=utf-8
from datetime import datetime

from flask import g, has_request_context

from .main import db


def get_current_user():
    if has_request_context():
        return g.user.id if g.user else None
    return None


class AuditableMixin(object):

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False,
                            onupdate=datetime.utcnow)
    created_by_id = db.Column(db.Integer, default=get_current_user)
    modified_by_id = db.Column(db.Integer, onupdate=get_current_user)

    @property
    def created_by(self):
        from ..auth.models.auth import User

        if not self.created_by_id:
            return None
        return User.by_id(self.created_by_id)

    @property
    def created_by_login(self):
        user = self.created_by
        if not user:
            return u''
        return user.login
