import logging
import sys

import colorama
import inflection
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.util import OrderedSet

from config import config
from db import query

db_engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    echo=config.SQLALCHEMY_ECHO,
    convert_unicode=True,
)
Session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=db_engine,
        query_cls=query.Query,
    )
)


class DeclarativeBase(object):
    exclude_modules = OrderedSet(['db', 'models'])

    @declared_attr
    def __tablename__(self):
        names = self.__module__.split('.') + inflection.underscore(self.__name__).split('_')
        names = list(OrderedSet(names) - self.exclude_modules)
        names[-1] = inflection.pluralize(names[-1])
        return '_'.join(names)


class Base(declarative_base(cls=DeclarativeBase, metadata=MetaData()), object):
    __abstract__ = True
    query = Session.query_property()


if config.SQLALCHEMY_ECHO:
    logger = logging.getLogger('sqlalchemy.engine.base.Engine')
    logger.setLevel(logging.INFO)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        ''.join([
            colorama.Style.BRIGHT,
            colorama.Fore.MAGENTA,
            '%(asctime)s: ',
            colorama.Fore.CYAN,
            '%(message)s',
            colorama.Fore.RESET,
            colorama.Style.RESET_ALL
        ])
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
