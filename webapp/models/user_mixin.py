# coding=utf-8
from datetime import datetime

from ..database import db


class UserMixin(object):
    name = db.Column(db.Unicode)
    email = db.Column(db.Unicode, index=True)
    search_vector = db.Column(db.TSVectorType('name', 'email'))
    locale = db.Column(db.String(16))
    tzinfo = db.Column(db.String(16))
    created_at = db.Column(
        db.DateTime, nullable=False,
        default=datetime.utcnow
    )
    modified_at = db.Column(
        db.DateTime, nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    @classmethod
    def by_email(cls, email):
        return db.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_all(cls, deleted=False, order=None):
        q = db.query(cls)
        if deleted is not None:
            q = q.filter(cls.deleted == deleted)
        if order is None:
            order = cls.login
        return q.order_by(order)

    @classmethod
    def search_all(cls, sq):
        return db.query(cls).filter(cls.deleted == False).search(sq)

    def __repr__(self):
        return "<User {}>".format(self.login.encode('utf8'))
