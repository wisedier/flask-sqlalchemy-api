import logging

from sqlalchemy_utils import force_auto_coercion


def turn_off_alchemy_log():
    logger = logging.getLogger('sqlalchemy.engine.base.Engine')
    [logger.removeHandler(handler) for handler in logger.handlers]
    logger.addHandler(logging.NullHandler())


def import_models():
    force_auto_coercion()
    __import__('db.models', fromlist=['*'])
