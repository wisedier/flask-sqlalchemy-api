import time

import sqlalchemy as sa
from sqlalchemy import orm


class IdMixin(object):
    query: orm.Query
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    @classmethod
    def get(cls, _id):
        if (isinstance(_id, str) and _id.isdigit()) or isinstance(_id, (int, float,)):
            return cls.query.get(int(_id))


class TimestampMixin(object):
    created_at = sa.Column(
        sa.Integer,
        default=lambda: int(time.time()),
        nullable=False
    )
    updated_at = sa.Column(
        sa.Integer,
        default=lambda: int(time.time()),
        onupdate=lambda: int(time.time()),
        nullable=False
    )
