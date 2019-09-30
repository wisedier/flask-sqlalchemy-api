import sqlalchemy as sa

from db.base import Base
from db.mixins import IdMixin


class Author(Base, IdMixin):
    name = sa.Column(sa.String(128), nullable=False)
