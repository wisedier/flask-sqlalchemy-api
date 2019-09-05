from db.base import Base
from db.mixins import IdMixin

import sqlalchemy as sa


class Author(Base, IdMixin):
    name = sa.Column(sa.String(128), nullable=False)
