from flask import Blueprint, jsonify, url_for, redirect, render_template
from flask_cors import CORS
from flask_restful import Api
from flask_swagger import swagger

from app.resources.definitions import definitions
from config import config

api = None


def init_api(app):
    global api
    api_bp = Blueprint('api', __name__, url_prefix='/api')
    CORS(api_bp, **config.CORS)
    api = Api(api_bp)

    @app.route('/')
    def redirect_to_docs():
        return redirect(url_for('docs'))

    @app.route('/spec')
    def spec():
        swag = swagger(app)
        swag['info']['title'] = f'{config.NAME}:{config.ENV} API'
        swag['info']['version'] = '1.0.0'
        swag['schemes'] = ['http']
        swag['consumes'] = ['application/json']
        swag['produces'] = ['application/json']
        swag['definitions'] = definitions
        return jsonify(swag)

    @app.route('/docs')
    def docs():
        return render_template('swagger/index.html',
                               name=config.NAME, env=config.ENV,
                               swagger_spec_json_url=url_for('spec', _external=True))
