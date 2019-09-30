import hashlib
import time
import uuid
from typing import Optional

import sqlalchemy as sa

from config import config
from db.base import Base
from db.mixins import IdMixin


class User(Base, IdMixin):
    name = sa.Column(sa.String(32), nullable=False, unique=True)


class UserAccessToken(Base):
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(User.id, ondelete='CASCADE'),
        nullable=False,
        primary_key=True,
    )
    token = sa.Column(sa.String(64), nullable=False, unique=True)
    expiration_timestamp = sa.Column(sa.Integer, nullable=True)

    @property
    def is_expired(self):
        if self.expiration_timestamp is not None:
            return self.expiration_timestamp < int(time.time())
        return False

    def refresh(self, *, commit: bool = True):
        self.token = self.get_new_token()
        if config.DEFAULT_ACCESS_TOKEN_EXPIRATION_TIME:
            self.expiration_timestamp = int(time.time() +
                                            config.DEFAULT_ACCESS_TOKEN_EXPIRATION_TIME)
        return self.save(commit=commit)

    @classmethod
    def get_user_by_token(cls, token: Optional[str]) -> Optional['User']:
        if token is None or len(token) != 64:
            return None

        at = cls.query.filter(cls.token == token).first()
        if at is None:
            return None

        return User.query.filter(User.id == at.user_id).first()

    @classmethod
    def get_new_token(cls):
        while True:
            token = hashlib.sha256(uuid.uuid4().bytes).hexdigest()
            at = cls.query.filter(cls.token == token).first()
            if at is None:
                break
        return token

    @classmethod
    def issue(cls, user: 'User', *, commit: bool = True):
        token = cls.get_new_token()
        expiration_timestamp = None
        if config.DEFAULT_ACCESS_TOKEN_EXPIRATION_TIME:
            expiration_timestamp = int(time.time() + config.DEFAULT_ACCESS_TOKEN_EXPIRATION_TIME)
        return (cls
                .create(user_id=user.id,
                        token=token,
                        expiration_timestamp=expiration_timestamp)
                .save(commit=commit))
