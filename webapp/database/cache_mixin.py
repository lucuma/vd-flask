# coding=utf-8
from datetime import datetime

import dateutil.parser
from sqlalchemy import event

from ..helpers.cache import cache

from .main import db


class CacheMixin(object):

    @classmethod
    def get_last_modified_at(cls):
        last_modified_at = cache.get('{}.last_modified_at'.format(cls.__name__))
        if last_modified_at and isinstance(last_modified_at, basestring):
            last_modified_at = dateutil.parser.parse(last_modified_at)
        return last_modified_at or datetime.utcnow()

    @classmethod
    def set_last_modified_at(cls, now):
        cache.set('{}.last_modified_at'.format(cls.__name__), now.isoformat())


@event.listens_for(db.session, 'before_commit')
def _on_before_commit(session):
    now = datetime.utcnow()
    for target in session.dirty:
        if hasattr(target, '_invalidate_cache'):
            if getattr(target, '__cache_updated_on', None) != now:
                target.__cache_updated_on = now
                target._invalidate_cache(now)
