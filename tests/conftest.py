# coding=utf-8
import pytest

from load_test_data import load_test_data
from webapp.database import db as app_db


def setup_module(module):
    app_db.create_all()
    load_test_data()


def teardown_module(module):
    app_db.drop_all()


@pytest.fixture()
def db(request):
    app_db.session.begin(subtransactions=True)
    request.addfinalizer(app_db.rollback)
    request.addfinalizer(app_db.session.close)
    return app_db
