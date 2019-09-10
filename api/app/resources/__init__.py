from argparse import Namespace
from base64 import b64decode
from functools import wraps
from typing import Optional

from flask import Response, request
from flask.json import JSONEncoder
from flask_restful import Resource, abort
from werkzeug.exceptions import BadRequest, NotFound

from app import status
from app.exc import APIError
from config import config
from db.exc import DBError
from db.models import UserAccessToken

__all__ = (
    'login_required',
    'APIResource',
)


def login_required(func):
    @wraps(func)
    def check_authorization(*args, **kwargs):
        user = APIResource.get_user()
        if user is None:
            return abort(403)
        return func(*args, **kwargs)
    return check_authorization


class APIResource(Resource):

    @property
    def ip_address(self):
        return request.environ.get('REMOTE_ADDR', None)

    def dispatch_request(self, *args, **kwargs):
        common_processor = getattr(self, 'common', None)
        try:
            if common_processor is not None:
                args, kwargs = common_processor(*args, **kwargs)
            response = super().dispatch_request(*args, **kwargs)
        except APIError as exc:
            return self.error_response(exc)
        except DBError as exc:
            return self.error_response(exc, status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            if isinstance(exc, (NotFound, BadRequest)):
                return self.error_response(exc)
            if config.DEBUG:
                raise
            return self.error_response(APIError())

        try:
            response, code = response
        except ValueError:
            code = status.HTTP_200_OK
        return response, code

    @classmethod
    def error_response(cls, exc, status_code=None):
        if status_code is None:
            status_code = exc.code

        description = exc.description
        data = dict(code=exc.__class__.__name__, description=description)
        data = JSONEncoder().encode(data)
        resp = Response(
            response=data,
            status=status_code,
            mimetype='application/json'
        )
        return resp

    @staticmethod
    def get_page(args: Namespace, default_page: int = 1):
        page = args.page
        return default_page if page is None or page <= 0 else page

    @staticmethod
    def get_per_page(args: Namespace, default_per_page: int = 10):
        per_page = args.per_page
        return default_per_page if per_page is None or per_page <= 0 else per_page

    @staticmethod
    def get_token() -> Optional[str]:
        authorization = request.headers.get('Authorization', '')
        if not authorization:
            return None

        try:
            bearer = authorization.split(' ')[1]
        except IndexError:
            return None

        try:
            return b64decode(bearer.encode())
        except (UnicodeEncodeError, ValueError):
            return None

    @staticmethod
    def get_user(token=None):
        if token is None:
            token = APIResource.get_token()
        return UserAccessToken.get_user_by_token(token)
