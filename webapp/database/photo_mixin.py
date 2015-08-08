# coding=utf-8
import os

from sqlalchemy.orm import validates

from .. import config

from .main import db


class PhotoMixin(object):

    photo = db.Column(db.Unicode, nullable=True)

    @validates('photo')
    def _remove_old_photo(self, key, value):
        if self.photo:
            external = self.photo.startswith((u'http://', u'http://'))
            if self.photo != value and not external:
                self.remove_file(self.photo)
        return value

    def remove_file(self):
        fullpath = os.path.join(config.UPLOADS_PATH, self.photo)
        try:
            os.remove(fullpath)
        except OSError:
            pass
