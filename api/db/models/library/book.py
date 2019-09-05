import sqlalchemy as sa
from sqlalchemy import UniqueConstraint, orm, String

from db.base import Base
from db.mixins import IdMixin
from db.models.library.author import Author


class Book(Base, IdMixin):
    name = sa.Column(sa.String(128), nullable=False)
    author_id = sa.Column(sa.Integer, sa.ForeignKey(Author.id, ondelete='CASCADE'), nullable=False)
    author = orm.relationship(Author)
    edition = sa.Column(String(16), nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint(name, author_id, edition),
    )
