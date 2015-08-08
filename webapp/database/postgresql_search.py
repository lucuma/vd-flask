# coding=utf-8
from sqlalchemy_searchable import search, make_searchable

from ..import config
from ..helpers.slugify import slugify


PLURALS = (u'as', u'es', u'is', u'os', u'us')


def prepare_term(term):
    if term.endswith(PLURALS):
        term = term[:-2]
    elif len(term) > 4:
        term = term[:-1]
    return term


def clean_search_term(search_term):
    search_term = search_term or u''
    search_term = slugify(search_term[:100], space=' ')
    return ' '.join([
        prepare_term(term)
        for term in search_term.split(u' ')
    ])


if config.SQLALCHEMY_URI.startswith('postgresql:'):
    make_searchable()


class SearchableQuery(object):

    def search(self, search_term, **kwargs):
        """Search given query with full text search.
        """
        search_term = clean_search_term(search_term)
        return search(self, search_term, **kwargs)
