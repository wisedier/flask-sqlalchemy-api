import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from sqlalchemy_utils import create_database, database_exists, drop_database

from api.app.wsgi import app
from config import config
from db import base
from db.base import Base
from utils.sqlalchemy import import_models, turn_off_alchemy_log

manager = Manager(app)
migrate = Migrate(
    app=app,
    db=base.db_engine,
    directory=os.path.join(config.PROJECT_ROOT, 'db', 'migrations'),
)
manager.add_command('db', MigrateCommand)
banner = u'\n'.join(
    [
        u"%-15s: %s" % (u'ENV', config.ENV),
        u"%-15s: %s" % (u'DB_ENGINE', base.db_engine)
    ]
)


def make_context():
    from sqlalchemy import orm

    models = __import__('db.models', fromlist=['*'])
    context = dict(
        app=app,
        config=config,
        db_engine=base.db_engine,
        db_session=base.Session,
        contains_eager=orm.contains_eager,
        joinedload=orm.joinedload,
        joinedload_all=orm.joinedload_all,
        aliased=orm.aliased,
    )
    for model in [models]:
        for key in dir(model):
            context[key] = getattr(model, key)
    return context


manager.add_command(
    'shell',
    Shell(banner=banner, make_context=make_context, use_ipython=False, use_bpython=False),
)


@manager.command
def run():
    app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        debug=config.DEBUG,
        use_debugger=config.DEBUG,
        use_reloader=True,
        threaded=True,
    )


@manager.command
def initdb():
    turn_off_alchemy_log()
    import_models()
    print("[*] Creating database...", end='')
    if not database_exists(config.SQLALCHEMY_DATABASE_URI):
        create_database(config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(bind=base.db_engine)
    print("Done")


@manager.command
def dropdb():
    turn_off_alchemy_log()
    import_models()
    print("[*] Dropping database...", end='')
    if database_exists(config.SQLALCHEMY_DATABASE_URI):
        drop_database(config.SQLALCHEMY_DATABASE_URI)
    print("Done")


@manager.command
def resetdb():
    dropdb()
    initdb()


if __name__ == '__main__':
    manager.run()
