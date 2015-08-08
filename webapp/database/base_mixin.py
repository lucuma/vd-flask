# coding=utf-8
from .main import db
from .dict_serializable import DictSerializable


class BaseMixin(DictSerializable):

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def by_id(cls, pk):
        return db.query(cls).get(pk)

    def __repr__(self):
        pkeys = [_ for _ in self.__table__.c if _.primary_key]
        items = [(_.name, getattr(self, _.name))
                 for _ in pkeys]
        return "{0}({1})".format(
            self.__class__.__name__,
            ', '.join(['{0}={1!r}'.format(*_) for _ in items]))
