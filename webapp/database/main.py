# coding=utf-8
import sqlalchemy as sa
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_wrapper import SQLAlchemy
from sqlalchemy_wrapper.helpers import BaseQuery

from ..import config
from ..app import app
from .postgresql_search import SearchableQuery


class Query(BaseQuery, SearchableQuery):
    pass


db = SQLAlchemy(
    config.SQLALCHEMY_URI, app, echo=config.SQLALCHEMY_ECHO, query_cls=Query,
)

sa.TSVectorType = TSVectorType
db.TSVectorType = TSVectorType
