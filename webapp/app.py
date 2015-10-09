# coding=utf-8
from flask import Flask, request
from allspeak import Allspeak
from moar import Thumbnailer
# from moar.engines.wand_engine import WandEngine
from typogrify.filters import (
    amp, caps, initial_quotes, smartypants, titlecase, typogrify, widont)

from . import config
from .helpers.cache import cache
from .helpers.flash import get_flashed_messages
from .helpers.jinja_fragment_cache import FragmentKeyBasedCacheExtension
from .helpers.jinja_includewith import IncludeWith
from .helpers.static import static_url, upload_url
from .helpers.templates import active, link_to, format_file_size, dumb_pluralize
from .helpers.urls import get_current_url


app = Flask(
    __name__,
    template_folder=config.TEMPLATES_PATH,
    static_folder=config.STATIC_PATH,
    static_url_path=config.STATIC_URL
)

app.config.from_object(config)

speak = Allspeak(
    config.LOCALES_PATH,
    get_request=lambda: request,
    default_locale=config.DEFAULT_LOCALE,
    default_timezone=config.DEFAULT_TIMEZONE
)

thumbnail = Thumbnailer(config.UPLOADS_PATH, config.UPLOADS_URL)
# thumbnail = Thumbnailer(config.UPLOADS_PATH, config.UPLOADS_URL, engine=WandEngine)

app.jinja_env.add_extension(FragmentKeyBasedCacheExtension)
app.jinja_env.fragment_cache = cache

app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.add_extension('jinja2.ext.with_')
app.jinja_env.add_extension(IncludeWith)


TEMPLATE_GLOBALS = {
    'active': active,
    'dumb_pluralize': dumb_pluralize,
    'link_to': link_to,
    'get_current_url': get_current_url,
    'get_flashed_messages': get_flashed_messages,
    'thumbnail': thumbnail,
}

TEMPLATE_FILTERS = {
    'static_url': static_url,
    'upload_url': upload_url,

    'file_size': format_file_size,
    'format': speak.format,
    'format_datetime': speak.format_datetime,
    'format_date': speak.format_date,
    'format_time': speak.format_time,
    'format_timedelta': speak.format_timedelta,
    'format_number': speak.format_number,
    'format_decimal': speak.format_decimal,
    'format_currency': speak.format_currency,
    'format_percent': speak.format_percent,
    'format_scientific': speak.format_scientific,

    'amp': amp,
    'caps': caps,
    'initial_quotes': initial_quotes,
    'smartypants': smartypants,
    'titlecase': titlecase,
    'typogrify': typogrify,
    'widont': widont,

    'dumb_pluralize': dumb_pluralize,

}
TEMPLATE_TESTS = {}

app.jinja_env.globals.update(TEMPLATE_GLOBALS)
app.jinja_env.filters.update(TEMPLATE_FILTERS)
app.jinja_env.tests.update(TEMPLATE_TESTS)
