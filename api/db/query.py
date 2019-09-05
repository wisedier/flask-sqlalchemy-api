import marshmallow
from sqlalchemy import orm

from db import utils

__all__ = (
    'Query',
)


class Query(orm.Query):

    def paginate(self, page=1, per_page=20, item_schema: marshmallow.Schema = None):
        """
        Returns `per_page` items from page `page`

        Args:
            page (int): page number
            per_page (int): the number of items per each page
            item_schema (:obj:`marshmallow.Schema`, optional): schema object to serialize

        Returns:
            :class:`Pagination` object

        Examples:
            >>> import marshmallow as mm
            >>> from db.models.account import User
            >>> class UserSchema(mm.Schema):
            ...     id = mm.fields.Int()
            ...     name = mm.fields.Str()
            ...
            >>> schema = UserSchema(many=True)
            >>> users = User.query.paginate(page=1, per_page=5, item_schema=schema).to_dict()
        """
        items = self.limit(per_page).offset((page - 1) * per_page).all()

        if not items and page != 1:
            return utils.Pagination(self, page, per_page, 0, [], item_schema)

        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = self.order_by(None).count()

        return utils.Pagination(self, page, per_page, total, items, item_schema)
