import importlib
import os
import sys

from flask import Flask, Response
from flask.json import JSONEncoder

from api.app import ext
from config import config
from db.base import session


def create_app():
    app = Flask(__name__)
    init_config(app)
    init_extensions(app)
    init_teardown(app)
    init_health_check(app)
    init_resources(app)
    return app


def init_config(app):
    app.config.from_object(config)


def init_teardown(app):
    @app.teardown_request
    def session_clear(response_or_exc):
        try:
            if response_or_exc is None:
                session.commit()
        finally:
            session.close()
        return response_or_exc


def init_health_check(app):
    @app.route('/healthz')
    def health_check():
        return 'ok'


def init_extensions(app):
    ext.init_api(app)


def init_resources(app):
    top_package_name = 'resources'

    def recursive_import(packages, parent_path=None):
        exclude_modules = {'__init__.py'}
        if parent_path is None:
            parent_path = os.path.join(app.root_path, top_package_name)

        for pkg in packages:
            pkg_path = os.path.join(parent_path, pkg)

            if os.path.isdir(pkg_path):
                sub_packages = os.listdir(pkg_path)
                recursive_import(sub_packages, pkg_path)
            else:
                if not pkg.endswith('.py') or pkg in exclude_modules:
                    continue

                module_path = (
                    __name__ +
                    pkg_path
                    .replace(os.path.normpath(app.root_path), '')
                    .replace(os.sep, '.')
                    .rstrip('.py')
                )
                if module_path in sys.modules:
                    importlib.reload(sys.modules[module_path])
                importlib.__import__(module_path, fromlist=['*'])

    top_packages = []
    try:
        top_packages = os.listdir(os.path.join(app.root_path, top_package_name))
    except OSError:
        app.logger.info(f"Directory '{top_package_name}' not found.")

    recursive_import(top_packages)

    app.register_blueprint(ext.api.blueprint)

    @ext.api.representation('application/json')
    def make_response(data, code, headers):
        resp = Response(
            response=JSONEncoder().encode(data),
            status=code,
            mimetype='application/json'
        )
        resp.headers.extend(headers or {})
        return resp
