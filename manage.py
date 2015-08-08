# coding=utf-8
from __future__ import print_function
import io
import os
from os.path import dirname, join

from alembic import command
from alembic.config import Config
import baker

from webapp.main import app
from webapp.auth import manage


@baker.command
def syncdb(revision='head'):
    """Run the database migrations
    """
    print('\n-- Updating to the latest revision --')
    alembic_cfg = Config(join(dirname(__file__), 'alembic.ini'))
    command.upgrade(alembic_cfg, revision)

    print('\n-- Done. --\n')


@baker.command
def revertdb(revision):
    """Revert the database to the given revision
    """
    print('\n-- Downgrade --')
    alembic_cfg = Config(join(dirname(__file__), 'alembic.ini'))
    command.downgrade(alembic_cfg, revision)

    print('\n-- Done. --\n')


@baker.command
def run(host='0.0.0.0', port=None, **kwargs):
    """Runs the application on the local development server.
    """
    try:
        port = int(port) if port else None
    except (ValueError, TypeError):
        port = None
    app.run(host, port, **kwargs)


@baker.command
def set_env(env):
    """Set the current environment.
    """
    from webapp.config import APP_ENV, ENV_FILE

    with io.open(ENV_FILE, 'wt') as f:
        f.write(unicode(env))
        os.environ[APP_ENV] = env
    print('APP_ENV is now {0}'.format(env))


@baker.command
def get_env():
    """Print the current environment.
    """
    from webapp.config import get_env

    print('APP_ENV is {0}'.format(get_env()))


@baker.command
def load_data():
    """Load initial data
    """
    from data import load_data

    print('\n-- Loading initial data. --\n')
    load_data()
    print('\n-- Done. --\n')


@baker.command
def assets(*args):
    """Manage the assets.
    """
    from webassets import script
    from webapp.assets import assets_env

    script.main(args, env=assets_env)


if __name__ == "__main__":
    baker.run()
