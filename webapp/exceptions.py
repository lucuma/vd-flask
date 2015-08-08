# coding=utf-8
from werkzeug.exceptions import *

from . import config


class DataNotFound(Exception):
    """A custom exception, to differentiate it from a real
    `HTTP 404: NOT FOUND` while debugging.
    """


if not config.DEBUG:
    DataNotFound = NotFound
