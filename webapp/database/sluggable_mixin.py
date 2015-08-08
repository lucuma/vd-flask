# coding=utf-8
from sqlalchemy.orm import validates

from ..helpers.slugify import slugify

from .main import db


class SluggableMixin(object):

    slug = db.Column(db.String, nullable=False, index=True)

    @property
    def _sluggable_query(self):
        return db.query(self.__class__)

    @validates('name')
    def _set_slug(self, key, value):
        """Update the slug when the name change."""
        self.slug = self._get_slug(value)
        return value

    @validates('slug')
    def _force_set_slug(self, key, value):
        """Force the slug to have a value"""
        return value or self._get_slug(self.name)

    def _get_slug(self, name):
        cls = self.__class__
        oslug = slugify(name or u'nn').lower()
        if self.slug == oslug:
            return oslug
        slug = oslug
        num = 1
        with db.session.no_autoflush:
            query = self._sluggable_query.filter(cls.id != self.id)
            while query.filter_by(slug=slug).count():
                slug = '{0}-{1}'.format(oslug, num)
                num = num + 1
        return slug

    @classmethod
    def by_slug(cls, slug, **kwargs):
        q = db.query(cls).filter(cls.slug == slug)
        return q.first()

    @classmethod
    def by_name(cls, name, **kwargs):
        slug = slugify(name)
        if not slug:
            return None
        return cls.by_slug(slug, **kwargs)
